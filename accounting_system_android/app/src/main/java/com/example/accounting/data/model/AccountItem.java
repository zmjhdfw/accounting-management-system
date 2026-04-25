package com.example.accounting.data.model;

import androidx.annotation.NonNull;

/**
 * 科目数据模型类
 * 封装科目的属性和序列化方法
 */
public class AccountItem {
    private String code;        // 科目代码
    private String name;        // 科目名称
    private String type;        // 科目类型（资产/负债/所有者权益/收入/费用）
    private double balance;     // 余额
    private String direction;   // 余额方向（借/贷）
    
    /**
     * 构造函数（自动推断类型和方向）
     */
    public AccountItem(String code, String name) {
        this.code = code;
        this.name = name;
        this.type = getAccountType(code);
        this.balance = 0.0;
        this.direction = getAccountDirection(code);
    }
    
    /**
     * 构造函数（完整参数）
     */
    public AccountItem(String code, String name, String type, double balance, String direction) {
        this.code = code;
        this.name = name;
        this.type = type;
        this.balance = balance;
        this.direction = direction;
    }
    
    // Getter方法
    public String getCode() { return code; }
    public String getName() { return name; }
    public String getType() { return type; }
    public double getBalance() { return balance; }
    public String getDirection() { return direction; }
    
    // Setter方法
    public void setCode(String code) { this.code = code; }
    public void setName(String name) { this.name = name; }
    public void setType(String type) { this.type = type; }
    public void setBalance(double balance) { this.balance = balance; }
    public void setDirection(String direction) { this.direction = direction; }
    
    /**
     * 序列化方法：将对象序列化为字符串
     * 格式：code:name:type:balance:direction
     */
    public String serialize() {
        return code + ":" + name + ":" + type + ":" + balance + ":" + direction;
    }
    
    /**
     * 反序列化方法：从字符串反序列化对象
     * @param str 序列化字符串
     * @return AccountItem对象，解析失败返回null
     */
    public static AccountItem deserialize(String str) {
        if (str == null || str.isEmpty()) return null;
        
        String[] parts = str.split(":");
        if (parts.length >= 5) {
            try {
                return new AccountItem(
                    parts[0],
                    parts[1],
                    parts[2],
                    Double.parseDouble(parts[3]),
                    parts[4]
                );
            } catch (NumberFormatException e) {
                return null;
            }
        }
        return null;
    }
    
    /**
     * 根据科目代码判断科目类型
     */
    public static String getAccountType(String code) {
        if (code == null || code.isEmpty()) return "未知";
        char first = code.charAt(0);
        switch (first) {
            case '1': return "资产";
            case '2': return "负债";
            case '3': return "所有者权益";
            case '4': return "收入";
            case '5': return "费用";
            default: return "未知";
        }
    }
    
    /**
     * 根据科目代码判断余额方向
     */
    public static String getAccountDirection(String code) {
        if (code == null || code.isEmpty()) return "借";
        char first = code.charAt(0);
        // 资产、费用类为借方余额
        // 负债、所有者权益、收入类为贷方余额
        return (first == '1' || first == '5') ? "借" : "贷";
    }
    
    @NonNull
    @Override
    public String toString() {
        return String.format("%s %s\n类型: %s | 余额: %.2f | 方向: %s", 
            code, name, type, balance, direction);
    }
}
