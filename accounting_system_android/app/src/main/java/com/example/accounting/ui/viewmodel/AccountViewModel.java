package com.example.accounting.ui.viewmodel;

import android.app.Application;
import androidx.annotation.NonNull;
import androidx.lifecycle.AndroidViewModel;
import androidx.lifecycle.LiveData;
import androidx.lifecycle.MutableLiveData;
import com.example.accounting.data.model.AccountItem;
import com.example.accounting.data.repository.AccountRepository;
import java.util.List;

/**
 * 科目ViewModel类
 * 管理UI数据，在配置变更时存活，通过Repository访问数据
 */
public class AccountViewModel extends AndroidViewModel {
    private AccountRepository repository;
    private LiveData<List<AccountItem>> accountsLiveData;
    private MutableLiveData<String> errorMessage;
    
    /**
     * 构造函数
     */
    public AccountViewModel(@NonNull Application application) {
        super(application);
        repository = AccountRepository.getInstance(application);
        accountsLiveData = repository.getAccountsLiveData();
        errorMessage = new MutableLiveData<>();
    }
    
    /**
     * 获取科目列表LiveData
     */
    public LiveData<List<AccountItem>> getAccounts() {
        return accountsLiveData;
    }
    
    /**
     * 获取错误消息LiveData
     */
    public LiveData<String> getErrorMessage() {
        return errorMessage;
    }
    
    /**
     * 添加科目
     */
    public void addAccount(AccountItem account) {
        repository.addAccount(account, new AccountRepository.Callback() {
            @Override
            public void onSuccess() {
                // LiveData自动更新，无需操作
            }
            
            @Override
            public void onError(String message) {
                errorMessage.postValue(message);
            }
        });
    }
    
    /**
     * 更新科目
     */
    public void updateAccount(AccountItem account) {
        repository.updateAccount(account, new AccountRepository.Callback() {
            @Override
            public void onSuccess() {
                // LiveData自动更新，无需操作
            }
            
            @Override
            public void onError(String message) {
                errorMessage.postValue(message);
            }
        });
    }
    
    /**
     * 删除科目
     */
    public void deleteAccount(String code) {
        repository.deleteAccount(code, new AccountRepository.Callback() {
            @Override
            public void onSuccess() {
                // LiveData自动更新，无需操作
            }
            
            @Override
            public void onError(String message) {
                errorMessage.postValue(message);
            }
        });
    }
}
