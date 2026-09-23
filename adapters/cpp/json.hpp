#pragma once

#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <map>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

class Json {
public:
    enum class Type { Null, Bool, Number, String, Array, Object };
    using Array = std::vector<Json>;
    using Object = std::map<std::string, Json>;

    Json() = default;
    Json(std::nullptr_t) : type_(Type::Null) {}
    Json(bool value) : type_(Type::Bool), bool_(value) {}
    Json(double value) : type_(Type::Number), num_(value) {}
    Json(int value) : type_(Type::Number), num_(value) {}
    Json(long long value) : type_(Type::Number), num_(static_cast<double>(value)) {}
    Json(const char* value) : type_(Type::String), str_(value) {}
    Json(std::string value) : type_(Type::String), str_(std::move(value)) {}
    Json(Array value) : type_(Type::Array), arr_(std::move(value)) {}
    Json(Object value) : type_(Type::Object), obj_(std::move(value)) {}

    static Json array() {
        Json value;
        value.type_ = Type::Array;
        return value;
    }

    static Json object() {
        Json value;
        value.type_ = Type::Object;
        return value;
    }

    static Json parse(const std::string& text) {
        size_t pos = 0;
        Json value = parse_value(text, pos);
        skip_whitespace(text, pos);
        if (pos != text.size()) {
            throw std::runtime_error("unexpected trailing characters");
        }
        return value;
    }

    Type type() const { return type_; }
    bool is_null() const { return type_ == Type::Null; }
    bool is_bool() const { return type_ == Type::Bool; }
    bool is_number() const { return type_ == Type::Number; }
    bool is_string() const { return type_ == Type::String; }
    bool is_array() const { return type_ == Type::Array; }
    bool is_object() const { return type_ == Type::Object; }

    bool as_bool() const { require(Type::Bool); return bool_; }
    double as_double() const { require(Type::Number); return num_; }
    long long as_int() const { require(Type::Number); return static_cast<long long>(num_); }
    const std::string& as_string() const { require(Type::String); return str_; }
    const Array& as_array() const { require(Type::Array); return arr_; }
    const Object& as_object() const { require(Type::Object); return obj_; }

    bool contains(const std::string& key) const {
        return type_ == Type::Object && obj_.find(key) != obj_.end();
    }

    const Json& operator[](const std::string& key) const {
        static const Json null_value;
        if (type_ != Type::Object) return null_value;
        auto it = obj_.find(key);
        return it == obj_.end() ? null_value : it->second;
    }

    Json& operator[](const std::string& key) {
        if (type_ != Type::Object) {
            *this = object();
        }
        return obj_[key];
    }

    void push_back(Json value) {
        if (type_ != Type::Array) {
            *this = array();
        }
        arr_.push_back(std::move(value));
    }

    std::string dump() const {
        std::string out;
        write_to(out);
        return out;
    }

private:
    void require(Type expected) const {
        if (type_ != expected) throw std::runtime_error("JSON type mismatch");
    }

    static void skip_whitespace(const std::string& text, size_t& pos) {
        while (pos < text.size() &&
               (text[pos] == ' ' || text[pos] == '\t' || text[pos] == '\n' || text[pos] == '\r')) {
            ++pos;
        }
    }

    static Json parse_value(const std::string& text, size_t& pos) {
        skip_whitespace(text, pos);
        if (pos >= text.size()) throw std::runtime_error("unexpected end of JSON");
        char c = text[pos];
        if (c == '{') return parse_object(text, pos);
        if (c == '[') return parse_array(text, pos);
        if (c == '"') return Json(parse_string(text, pos));
        if (c == 't') { expect_literal(text, pos, "true"); return Json(true); }
        if (c == 'f') { expect_literal(text, pos, "false"); return Json(false); }
        if (c == 'n') { expect_literal(text, pos, "null"); return Json(); }
        if (c == '-' || (c >= '0' && c <= '9')) return parse_number(text, pos);
        throw std::runtime_error("unexpected character in JSON");
    }

    static void expect_literal(const std::string& text, size_t& pos, const std::string& literal) {
        if (text.compare(pos, literal.size(), literal) != 0) {
            throw std::runtime_error("invalid literal");
        }
        pos += literal.size();
    }

    static Json parse_number(const std::string& text, size_t& pos) {
        size_t start = pos;
        if (text[pos] == '-') ++pos;
        while (pos < text.size() &&
               ((text[pos] >= '0' && text[pos] <= '9') || text[pos] == '.' ||
                text[pos] == 'e' || text[pos] == 'E' || text[pos] == '+' || text[pos] == '-')) {
            ++pos;
        }
        return Json(std::stod(text.substr(start, pos - start)));
    }

    static std::string parse_string(const std::string& text, size_t& pos) {
        if (text[pos] != '"') throw std::runtime_error("expected string");
        ++pos;
        std::string out;
        while (pos < text.size()) {
            char c = text[pos++];
            if (c == '"') return out;
            if (c != '\\') {
                out.push_back(c);
                continue;
            }
            if (pos >= text.size()) throw std::runtime_error("bad escape");
            char esc = text[pos++];
            switch (esc) {
                case '"': out.push_back('"'); break;
                case '\\': out.push_back('\\'); break;
                case '/': out.push_back('/'); break;
                case 'b': out.push_back('\b'); break;
                case 'f': out.push_back('\f'); break;
                case 'n': out.push_back('\n'); break;
                case 'r': out.push_back('\r'); break;
                case 't': out.push_back('\t'); break;
                case 'u': {
                    unsigned int cp = parse_hex4(text, pos);
                    if (cp >= 0xD800 && cp <= 0xDBFF) {
                        if (pos + 1 < text.size() && text[pos] == '\\' && text[pos + 1] == 'u') {
                            pos += 2;
                            unsigned int low = parse_hex4(text, pos);
                            if (low >= 0xDC00 && low <= 0xDFFF) {
                                cp = 0x10000 + ((cp - 0xD800) << 10) + (low - 0xDC00);
                            } else {
                                throw std::runtime_error("invalid surrogate pair");
                            }
                        } else {
                            throw std::runtime_error("unpaired surrogate");
                        }
                    }
                    append_utf8(out, cp);
                    break;
                }
                default: throw std::runtime_error("invalid escape");
            }
        }
        throw std::runtime_error("unterminated string");
    }

    static unsigned int parse_hex4(const std::string& text, size_t& pos) {
        if (pos + 4 > text.size()) throw std::runtime_error("bad \\u escape");
        unsigned int value = 0;
        for (int i = 0; i < 4; ++i) {
            char c = text[pos++];
            value <<= 4;
            if (c >= '0' && c <= '9') value |= static_cast<unsigned int>(c - '0');
            else if (c >= 'a' && c <= 'f') value |= static_cast<unsigned int>(c - 'a' + 10);
            else if (c >= 'A' && c <= 'F') value |= static_cast<unsigned int>(c - 'A' + 10);
            else throw std::runtime_error("bad \\u escape");
        }
        return value;
    }

    static void append_utf8(std::string& out, unsigned int cp) {
        if (cp < 0x80) {
            out.push_back(static_cast<char>(cp));
        } else if (cp < 0x800) {
            out.push_back(static_cast<char>(0xC0 | (cp >> 6)));
            out.push_back(static_cast<char>(0x80 | (cp & 0x3F)));
        } else if (cp < 0x10000) {
            out.push_back(static_cast<char>(0xE0 | (cp >> 12)));
            out.push_back(static_cast<char>(0x80 | ((cp >> 6) & 0x3F)));
            out.push_back(static_cast<char>(0x80 | (cp & 0x3F)));
        } else {
            out.push_back(static_cast<char>(0xF0 | (cp >> 18)));
            out.push_back(static_cast<char>(0x80 | ((cp >> 12) & 0x3F)));
            out.push_back(static_cast<char>(0x80 | ((cp >> 6) & 0x3F)));
            out.push_back(static_cast<char>(0x80 | (cp & 0x3F)));
        }
    }

    static Json parse_array(const std::string& text, size_t& pos) {
        ++pos;
        Json value = array();
        skip_whitespace(text, pos);
        if (pos < text.size() && text[pos] == ']') { ++pos; return value; }
        while (true) {
            value.arr_.push_back(parse_value(text, pos));
            skip_whitespace(text, pos);
            if (pos >= text.size()) throw std::runtime_error("unterminated array");
            if (text[pos] == ',') { ++pos; continue; }
            if (text[pos] == ']') { ++pos; return value; }
            throw std::runtime_error("expected ',' or ']'");
        }
    }

    static Json parse_object(const std::string& text, size_t& pos) {
        ++pos;
        Json value = object();
        skip_whitespace(text, pos);
        if (pos < text.size() && text[pos] == '}') { ++pos; return value; }
        while (true) {
            skip_whitespace(text, pos);
            if (pos >= text.size() || text[pos] != '"') throw std::runtime_error("expected key");
            std::string key = parse_string(text, pos);
            skip_whitespace(text, pos);
            if (pos >= text.size() || text[pos] != ':') throw std::runtime_error("expected ':'");
            ++pos;
            value.obj_[key] = parse_value(text, pos);
            skip_whitespace(text, pos);
            if (pos >= text.size()) throw std::runtime_error("unterminated object");
            if (text[pos] == ',') { ++pos; continue; }
            if (text[pos] == '}') { ++pos; return value; }
            throw std::runtime_error("expected ',' or '}'");
        }
    }

    void write_to(std::string& out) const {
        switch (type_) {
            case Type::Null: out += "null"; break;
            case Type::Bool: out += bool_ ? "true" : "false"; break;
            case Type::Number: {
                double integral = 0.0;
                if (num_ >= -9.007199254740992e15 && num_ <= 9.007199254740992e15) {
                    integral = static_cast<long long>(num_);
                }
                if (num_ == integral) {
                    out += std::to_string(static_cast<long long>(num_));
                } else {
                    char buf[32];
                    std::snprintf(buf, sizeof(buf), "%.15g", num_);
                    if (std::strtod(buf, nullptr) != num_) {
                        std::snprintf(buf, sizeof(buf), "%.17g", num_);
                    }
                    out += buf;
                }
                break;
            }
            case Type::String: write_string(out, str_); break;
            case Type::Array: {
                out += '[';
                for (size_t i = 0; i < arr_.size(); ++i) {
                    if (i > 0) out += ',';
                    arr_[i].write_to(out);
                }
                out += ']';
                break;
            }
            case Type::Object: {
                out += '{';
                bool first = true;
                for (const auto& entry : obj_) {
                    if (!first) out += ',';
                    first = false;
                    write_string(out, entry.first);
                    out += ':';
                    entry.second.write_to(out);
                }
                out += '}';
                break;
            }
        }
    }

    static void write_string(std::string& out, const std::string& s) {
        out += '"';
        for (unsigned char c : s) {
            switch (c) {
                case '"': out += "\\\""; break;
                case '\\': out += "\\\\"; break;
                case '\b': out += "\\b"; break;
                case '\f': out += "\\f"; break;
                case '\n': out += "\\n"; break;
                case '\r': out += "\\r"; break;
                case '\t': out += "\\t"; break;
                default:
                    if (c < 0x20) {
                        char buf[8];
                        std::snprintf(buf, sizeof(buf), "\\u%04x", c);
                        out += buf;
                    } else {
                        out += static_cast<char>(c);
                    }
            }
        }
        out += '"';
    }

    Type type_ = Type::Null;
    bool bool_ = false;
    double num_ = 0.0;
    std::string str_;
    Array arr_;
    Object obj_;
};
