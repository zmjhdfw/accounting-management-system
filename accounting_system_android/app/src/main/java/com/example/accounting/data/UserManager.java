package com.example.accounting.data;

import android.content.Context;
import android.content.SharedPreferences;
import java.util.ArrayList;
import java.util.List;

/**
 * 用户管理类
 */
public class UserManager {
    private static final String PREF_NAME = "user_prefs";
    private static final String KEY_USERS = "users";
    private static final String KEY_CURRENT_USER = "current_user";
    
    private SharedPreferences prefs;
    
    public UserManager(Context context) {
        prefs = context.getSharedPreferences(PREF_NAME, Context.MODE_PRIVATE);
    }
    
    // 用户数据类
    public static class User {
        public String username;
        public String password;
        public String nickname;
        public String email;
        
        public User(String username, String password) {
            this.username = username;
            this.password = password;
            this.nickname = username;
            this.email = "";
        }
        
        public User(String username, String password, String nickname, String email) {
            this.username = username;
            this.password = password;
            this.nickname = nickname;
            this.email = email;
        }
        
        @Override
        public String toString() {
            return username + ":" + password + ":" + nickname + ":" + email;
        }
        
        public static User fromString(String str) {
            String[] parts = str.split(":");
            if (parts.length >= 2) {
                User user = new User(parts[0], parts[1]);
                if (parts.length >= 3) user.nickname = parts[2];
                if (parts.length >= 4) user.email = parts[3];
                return user;
            }
            return null;
        }
    }
    
    // 获取所有用户
    public List<User> getAllUsers() {
        List<User> users = new ArrayList<>();
        String usersStr = prefs.getString(KEY_USERS, "");
        if (!usersStr.isEmpty()) {
            for (String userStr : usersStr.split(";")) {
                User user = User.fromString(userStr);
                if (user != null) users.add(user);
            }
        }
        return users;
    }
    
    // 保存所有用户
    private void saveAllUsers(List<User> users) {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < users.size(); i++) {
            if (i > 0) sb.append(";");
            sb.append(users.get(i).toString());
        }
        prefs.edit().putString(KEY_USERS, sb.toString()).apply();
    }
    
    // 注册用户
    public boolean register(String username, String password) {
        if (username.isEmpty() || password.isEmpty()) return false;
        
        List<User> users = getAllUsers();
        for (User user : users) {
            if (user.username.equals(username)) return false;
        }
        
        users.add(new User(username, password));
        saveAllUsers(users);
        return true;
    }
    
    // 登录验证
    public User login(String username, String password) {
        List<User> users = getAllUsers();
        for (User user : users) {
            if (user.username.equals(username) && user.password.equals(password)) {
                prefs.edit().putString(KEY_CURRENT_USER, username).apply();
                return user;
            }
        }
        return null;
    }
    
    // 获取当前用户
    public User getCurrentUser() {
        String username = prefs.getString(KEY_CURRENT_USER, "");
        if (username.isEmpty()) return null;
        
        List<User> users = getAllUsers();
        for (User user : users) {
            if (user.username.equals(username)) return user;
        }
        return null;
    }
    
    // 注销登录
    public void logout() {
        prefs.edit().remove(KEY_CURRENT_USER).apply();
    }
    
    // 更新用户信息
    public boolean updateUser(String username, String nickname, String email) {
        List<User> users = getAllUsers();
        for (User user : users) {
            if (user.username.equals(username)) {
                user.nickname = nickname;
                user.email = email;
                saveAllUsers(users);
                return true;
            }
        }
        return false;
    }
    
    // 修改密码
    public boolean changePassword(String username, String oldPassword, String newPassword) {
        List<User> users = getAllUsers();
        for (User user : users) {
            if (user.username.equals(username) && user.password.equals(oldPassword)) {
                user.password = newPassword;
                saveAllUsers(users);
                return true;
            }
        }
        return false;
    }
    
    // 删除用户
    public boolean deleteUser(String username) {
        List<User> users = getAllUsers();
        for (int i = 0; i < users.size(); i++) {
            if (users.get(i).username.equals(username)) {
                users.remove(i);
                saveAllUsers(users);
                return true;
            }
        }
        return false;
    }
}
