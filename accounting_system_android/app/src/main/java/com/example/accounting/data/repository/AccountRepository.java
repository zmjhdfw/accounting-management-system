package com.example.accounting.data.repository;

import android.content.Context;
import android.content.SharedPreferences;
import android.os.Handler;
import android.os.Looper;
import androidx.lifecycle.LiveData;
import androidx.lifecycle.MutableLiveData;
import com.example.accounting.data.model.AccountItem;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

/**
 * 科目数据仓库类
 * 封装数据访问逻辑，提供LiveData给ViewModel观察，实现数据的持久化和加载
 */
public class AccountRepository {
    private static final String PREF_NAME = "account_prefs";
    private static final String KEY_ACCOUNTS = "accounts";
    
    private static AccountRepository instance;
    private SharedPreferences prefs;
    private MutableLiveData<List<AccountItem>> accountsLiveData;
    private ExecutorService executor;
    
    /**
     * 回调接口
     */
    public interface Callback {
        void onSuccess();
        void onError(String message);
    }
    
    /**
     * 私有构造函数
     */
    private AccountRepository(Context context) {
        prefs = context.getSharedPreferences(PREF_NAME, Context.MODE_PRIVATE);
        accountsLiveData = new MutableLiveData<>();
        executor = Executors.newSingleThreadExecutor();
        loadAccounts();
    }
    
    /**
     * 获取单例实例
     */
    public static synchronized AccountRepository getInstance(Context context) {
        if (instance == null) {
            instance = new AccountRepository(context.getApplicationContext());
        }
        return instance;
    }
    
    /**
     * 加载科目数据
     */
    private void loadAccounts() {
        accountsLiveData.setValue(getAllAccounts());
    }
    
    /**
     * 从SharedPreferences读取所有科目
     */
    private List<AccountItem> getAllAccounts() {
        List<AccountItem> accounts = new ArrayList<>();
        String accountsStr = prefs.getString(KEY_ACCOUNTS, "");
        if (!accountsStr.isEmpty()) {
            for (String accountStr : accountsStr.split(";")) {
                AccountItem account = AccountItem.deserialize(accountStr);
                if (account != null) {
                    accounts.add(account);
                }
            }
        }
        return accounts;
    }
    
    /**
     * 保存所有科目到SharedPreferences
     */
    private void saveAllAccounts(List<AccountItem> accounts) {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < accounts.size(); i++) {
            if (i > 0) sb.append(";");
            sb.append(accounts.get(i).serialize());
        }
        prefs.edit().putString(KEY_ACCOUNTS, sb.toString()).apply();
    }
    
    /**
     * 获取科目LiveData
     */
    public LiveData<List<AccountItem>> getAccountsLiveData() {
        return accountsLiveData;
    }
    
    /**
     * 添加科目
     */
    public void addAccount(AccountItem account, Callback callback) {
        executor.execute(() -> {
            List<AccountItem> accounts = getAllAccounts();
            
            // 检查编码是否已存在
            for (AccountItem a : accounts) {
                if (a.getCode().equals(account.getCode())) {
                    notifyError(callback, "科目编码已存在");
                    return;
                }
            }
            
            // 添加科目
            accounts.add(account);
            saveAllAccounts(accounts);
            
            // 更新LiveData
            accountsLiveData.postValue(accounts);
            
            // 回调成功
            notifySuccess(callback);
        });
    }
    
    /**
     * 更新科目
     */
    public void updateAccount(AccountItem account, Callback callback) {
        executor.execute(() -> {
            List<AccountItem> accounts = getAllAccounts();
            
            // 查找并更新
            boolean found = false;
            for (int i = 0; i < accounts.size(); i++) {
                if (accounts.get(i).getCode().equals(account.getCode())) {
                    accounts.set(i, account);
                    found = true;
                    break;
                }
            }
            
            if (!found) {
                notifyError(callback, "科目不存在");
                return;
            }
            
            // 保存数据
            saveAllAccounts(accounts);
            
            // 更新LiveData
            accountsLiveData.postValue(accounts);
            
            // 回调成功
            notifySuccess(callback);
        });
    }
    
    /**
     * 删除科目
     */
    public void deleteAccount(String code, Callback callback) {
        executor.execute(() -> {
            List<AccountItem> accounts = getAllAccounts();
            
            // 查找并删除
            boolean found = false;
            for (int i = 0; i < accounts.size(); i++) {
                if (accounts.get(i).getCode().equals(code)) {
                    accounts.remove(i);
                    found = true;
                    break;
                }
            }
            
            if (!found) {
                notifyError(callback, "科目不存在");
                return;
            }
            
            // 保存数据
            saveAllAccounts(accounts);
            
            // 更新LiveData
            accountsLiveData.postValue(accounts);
            
            // 回调成功
            notifySuccess(callback);
        });
    }
    
    /**
     * 在主线程回调成功
     */
    private void notifySuccess(Callback callback) {
        if (callback != null) {
            new Handler(Looper.getMainLooper()).post(callback::onSuccess);
        }
    }
    
    /**
     * 在主线程回调错误
     */
    private void notifyError(Callback callback, String message) {
        if (callback != null) {
            new Handler(Looper.getMainLooper()).post(() -> callback.onError(message));
        }
    }
}
