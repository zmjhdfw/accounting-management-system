package com.example.accounting.data;

import android.content.Context;
import android.content.SharedPreferences;
import java.util.ArrayList;
import java.util.List;

/**
 * 科目管理类
 */
public class AccountManager {
    private static final String PREF_NAME = "account_prefs";
    private static final String KEY_ACCOUNTS = "accounts";
    
    private SharedPreferences prefs;
    
    public AccountManager(Context context) {
        prefs = context.getSharedPreferences(PREF_NAME, Context.MODE_PRIVATE);
    }
    
    // 科目数据类
    public static class AccountItem {
        public String code;
        public String name;
        public String type;
        public double balance;
        public String direction;
        
        public AccountItem(String code, String name, String type, double balance, String direction) {
            this.code = code;
            this.name = name;
            this.type = type;
            this.balance = balance;
            this.direction = direction;
        }
        
        @Override
        public String toString() {
            return code + ":" + name + ":" + type + ":" + balance + ":" + direction;
        }
        
        public static AccountItem fromString(String str) {
            String[] parts = str.split(":");
            if (parts.length >= 5) {
                return new AccountItem(
                    parts[0],
                    parts[1],
                    parts[2],
                    Double.parseDouble(parts[3]),
                    parts[4]
                );
            }
            return null;
        }
    }
    
    // 获取所有科目
    public List<AccountItem> getAllAccounts() {
        List<AccountItem> accounts = new ArrayList<>();
        String accountsStr = prefs.getString(KEY_ACCOUNTS, "");
        if (!accountsStr.isEmpty()) {
            for (String accountStr : accountsStr.split(";")) {
                AccountItem account = AccountItem.fromString(accountStr);
                if (account != null) accounts.add(account);
            }
        }
        return accounts;
    }
    
    // 保存所有科目
    private void saveAllAccounts(List<AccountItem> accounts) {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < accounts.size(); i++) {
            if (i > 0) sb.append(";");
            sb.append(accounts.get(i).toString());
        }
        prefs.edit().putString(KEY_ACCOUNTS, sb.toString()).apply();
    }
    
    // 添加科目
    public boolean addAccount(AccountItem account) {
        List<AccountItem> accounts = getAllAccounts();
        for (AccountItem a : accounts) {
            if (a.code.equals(account.code)) return false;
        }
        accounts.add(account);
        saveAllAccounts(accounts);
        return true;
    }
    
    // 更新科目
    public boolean updateAccount(AccountItem account) {
        List<AccountItem> accounts = getAllAccounts();
        for (int i = 0; i < accounts.size(); i++) {
            if (accounts.get(i).code.equals(account.code)) {
                accounts.set(i, account);
                saveAllAccounts(accounts);
                return true;
            }
        }
        return false;
    }
    
    // 删除科目
    public boolean deleteAccount(String code) {
        List<AccountItem> accounts = getAllAccounts();
        for (int i = 0; i < accounts.size(); i++) {
            if (accounts.get(i).code.equals(code)) {
                accounts.remove(i);
                saveAllAccounts(accounts);
                return true;
            }
        }
        return false;
    }
    
    // 根据编码获取科目
    public AccountItem getAccountByCode(String code) {
        List<AccountItem> accounts = getAllAccounts();
        for (AccountItem account : accounts) {
            if (account.code.equals(code)) return account;
        }
        return null;
    }
}
