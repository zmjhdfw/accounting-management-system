package com.example.accounting.ui;

import android.content.Intent;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;
import androidx.fragment.app.Fragment;
import com.google.android.material.bottomnavigation.BottomNavigationView;
import com.example.accounting.R;
import com.example.accounting.data.UserManager;

/**
 * 主Activity
 */
public class MainActivity extends AppCompatActivity {
    
    private UserManager userManager;
    private String currentUsername;
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        
        userManager = new UserManager(this);
        currentUsername = getIntent().getStringExtra("username");
        
        BottomNavigationView bottomNav = findViewById(R.id.bottom_navigation);
        bottomNav.setOnItemSelectedListener(item -> {
            Fragment selectedFragment = null;
            int itemId = item.getItemId();
            
            if (itemId == R.id.nav_account) {
                selectedFragment = new AccountFragment();
            } else if (itemId == R.id.nav_voucher) {
                selectedFragment = new VoucherFragment();
            } else if (itemId == R.id.nav_report) {
                selectedFragment = new ReportFragment();
            }
            
            if (selectedFragment != null) {
                getSupportFragmentManager().beginTransaction()
                    .replace(R.id.fragment_container, selectedFragment)
                    .commit();
            }
            
            return true;
        });
        
        // 默认显示科目管理
        if (savedInstanceState == null) {
            getSupportFragmentManager().beginTransaction()
                .replace(R.id.fragment_container, new AccountFragment())
                .commit();
        }
    }
    
    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.main_menu, menu);
        return true;
    }
    
    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        int id = item.getItemId();
        
        if (id == R.id.action_user_info) {
            showUserInfo();
            return true;
        } else if (id == R.id.action_logout) {
            logout();
            return true;
        }
        
        return super.onOptionsItemSelected(item);
    }
    
    private void showUserInfo() {
        UserManager.User user = userManager.getCurrentUser();
        if (user != null) {
            String info = "用户名: " + user.username + 
                         "\n昵称: " + user.nickname +
                         "\n邮箱: " + (user.email.isEmpty() ? "未设置" : user.email);
            Toast.makeText(this, info, Toast.LENGTH_LONG).show();
        }
    }
    
    private void logout() {
        userManager.logout();
        Intent intent = new Intent(this, LoginActivity.class);
        startActivity(intent);
        finish();
    }
}
