package com.example.accounting.ui;

import android.app.AlertDialog;
import android.app.Dialog;
import android.content.Intent;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.view.Window;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.Toolbar;
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
        
        // 设置Toolbar
        Toolbar toolbar = findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);
        
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
        
        if (id == R.id.action_account_info) {
            showAccountInfo();
            return true;
        } else if (id == R.id.action_edit_profile) {
            showEditProfile();
            return true;
        } else if (id == R.id.action_change_password) {
            showChangePassword();
            return true;
        } else if (id == R.id.action_delete_account) {
            showDeleteAccount();
            return true;
        } else if (id == R.id.action_logout) {
            logout();
            return true;
        }
        
        return super.onOptionsItemSelected(item);
    }
    
    private void showAccountInfo() {
        UserManager.User user = userManager.getCurrentUser();
        if (user != null) {
            new AlertDialog.Builder(this)
                .setTitle("账户信息")
                .setMessage("用户名: " + user.username + 
                           "\n昵称: " + user.nickname +
                           "\n邮箱: " + (user.email.isEmpty() ? "未设置" : user.email))
                .setPositiveButton("确定", null)
                .show();
        }
    }
    
    private void showEditProfile() {
        UserManager.User user = userManager.getCurrentUser();
        if (user == null) return;
        
        Dialog dialog = new Dialog(this);
        dialog.requestWindowFeature(Window.FEATURE_NO_TITLE);
        dialog.setContentView(R.layout.dialog_edit_profile);
        
        TextView usernameText = dialog.findViewById(R.id.username_text);
        EditText nicknameEdit = dialog.findViewById(R.id.nickname_edit);
        EditText emailEdit = dialog.findViewById(R.id.email_edit);
        Button cancelBtn = dialog.findViewById(R.id.cancel_button);
        Button saveBtn = dialog.findViewById(R.id.save_button);
        
        usernameText.setText(user.username);
        nicknameEdit.setText(user.nickname);
        emailEdit.setText(user.email);
        
        saveBtn.setOnClickListener(v -> {
            String nickname = nicknameEdit.getText().toString().trim();
            String email = emailEdit.getText().toString().trim();
            
            if (userManager.updateUser(user.username, nickname, email)) {
                Toast.makeText(this, "资料更新成功", Toast.LENGTH_SHORT).show();
                dialog.dismiss();
            } else {
                Toast.makeText(this, "更新失败", Toast.LENGTH_SHORT).show();
            }
        });
        
        cancelBtn.setOnClickListener(v -> dialog.dismiss());
        dialog.show();
    }
    
    private void showChangePassword() {
        UserManager.User user = userManager.getCurrentUser();
        if (user == null) return;
        
        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        builder.setTitle("修改密码");
        
        // 创建输入框
        final EditText oldPass = new EditText(this);
        oldPass.setHint("旧密码");
        oldPass.setInputType(android.text.InputType.TYPE_CLASS_TEXT | android.text.InputType.TYPE_TEXT_VARIATION_PASSWORD);
        
        final EditText newPass = new EditText(this);
        newPass.setHint("新密码");
        newPass.setInputType(android.text.InputType.TYPE_CLASS_TEXT | android.text.InputType.TYPE_TEXT_VARIATION_PASSWORD);
        
        final EditText confirmPass = new EditText(this);
        confirmPass.setHint("确认新密码");
        confirmPass.setInputType(android.text.InputType.TYPE_CLASS_TEXT | android.text.InputType.TYPE_TEXT_VARIATION_PASSWORD);
        
        android.widget.LinearLayout layout = new android.widget.LinearLayout(this);
        layout.setOrientation(android.widget.LinearLayout.VERTICAL);
        layout.setPadding(50, 40, 50, 10);
        layout.addView(oldPass);
        layout.addView(newPass);
        layout.addView(confirmPass);
        builder.setView(layout);
        
        builder.setPositiveButton("确定", (d, which) -> {
            String old = oldPass.getText().toString();
            String newP = newPass.getText().toString();
            String confirm = confirmPass.getText().toString();
            
            if (!newP.equals(confirm)) {
                Toast.makeText(this, "两次密码不一致", Toast.LENGTH_SHORT).show();
                return;
            }
            
            if (userManager.changePassword(user.username, old, newP)) {
                Toast.makeText(this, "密码修改成功", Toast.LENGTH_SHORT).show();
            } else {
                Toast.makeText(this, "旧密码错误", Toast.LENGTH_SHORT).show();
            }
        });
        builder.setNegativeButton("取消", null);
        builder.show();
    }
    
    private void showDeleteAccount() {
        UserManager.User user = userManager.getCurrentUser();
        if (user == null) return;
        
        new AlertDialog.Builder(this)
            .setTitle("注销账户")
            .setMessage("确定要注销账户吗？此操作不可恢复！")
            .setPositiveButton("注销", (d, w) -> {
                if (userManager.deleteUser(user.username)) {
                    Toast.makeText(this, "账户已注销", Toast.LENGTH_SHORT).show();
                    logout();
                } else {
                    Toast.makeText(this, "注销失败", Toast.LENGTH_SHORT).show();
                }
            })
            .setNegativeButton("取消", null)
            .show();
    }
    
    private void logout() {
        userManager.logout();
        Intent intent = new Intent(this, LoginActivity.class);
        startActivity(intent);
        finish();
    }
}
