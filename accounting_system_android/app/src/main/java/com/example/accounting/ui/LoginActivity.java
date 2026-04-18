package com.example.accounting.ui;

import android.app.Dialog;
import android.content.Intent;
import android.os.Bundle;
import android.view.Window;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;
import com.example.accounting.R;
import com.example.accounting.data.UserManager;

/**
 * 登录Activity
 */
public class LoginActivity extends AppCompatActivity {
    
    private EditText usernameEdit;
    private EditText passwordEdit;
    private Button loginButton;
    private Button registerButton;
    private UserManager userManager;
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);
        
        userManager = new UserManager(this);
        
        usernameEdit = findViewById(R.id.username_edit);
        passwordEdit = findViewById(R.id.password_edit);
        loginButton = findViewById(R.id.login_button);
        registerButton = findViewById(R.id.register_button);
        Button forgotPasswordButton = findViewById(R.id.forgot_password_button);
        
        loginButton.setOnClickListener(v -> {
            String username = usernameEdit.getText().toString().trim();
            String password = passwordEdit.getText().toString();
            
            if (username.isEmpty()) {
                Toast.makeText(this, "请输入用户名", Toast.LENGTH_SHORT).show();
                return;
            }
            
            if (password.isEmpty()) {
                Toast.makeText(this, "请输入密码", Toast.LENGTH_SHORT).show();
                return;
            }
            
            UserManager.User user = userManager.login(username, password);
            if (user != null) {
                Toast.makeText(this, "登录成功", Toast.LENGTH_SHORT).show();
                // 跳转到主界面
                Intent intent = new Intent(this, MainActivity.class);
                intent.putExtra("username", user.username);
                startActivity(intent);
                finish();
            } else {
                Toast.makeText(this, "用户名或密码错误", Toast.LENGTH_SHORT).show();
            }
        });
        
        registerButton.setOnClickListener(v -> showRegisterDialog());
        
        forgotPasswordButton.setOnClickListener(v -> 
            Toast.makeText(this, "请联系管理员重置密码", Toast.LENGTH_SHORT).show());
    }
    
    private void showRegisterDialog() {
        Dialog dialog = new Dialog(this);
        dialog.requestWindowFeature(Window.FEATURE_NO_TITLE);
        dialog.setContentView(R.layout.dialog_register);
        
        EditText regUsername = dialog.findViewById(R.id.username_edit);
        EditText regPassword = dialog.findViewById(R.id.password_edit);
        EditText regConfirm = dialog.findViewById(R.id.confirm_password_edit);
        Button cancelBtn = dialog.findViewById(R.id.cancel_button);
        Button registerBtn = dialog.findViewById(R.id.register_button);
        
        registerBtn.setOnClickListener(v -> {
            String username = regUsername.getText().toString().trim();
            String password = regPassword.getText().toString();
            String confirm = regConfirm.getText().toString();
            
            if (username.isEmpty()) {
                Toast.makeText(this, "请输入用户名", Toast.LENGTH_SHORT).show();
                return;
            }
            
            if (password.isEmpty()) {
                Toast.makeText(this, "请输入密码", Toast.LENGTH_SHORT).show();
                return;
            }
            
            if (!password.equals(confirm)) {
                Toast.makeText(this, "两次密码不一致", Toast.LENGTH_SHORT).show();
                return;
            }
            
            if (userManager.register(username, password)) {
                Toast.makeText(this, "注册成功，请登录", Toast.LENGTH_SHORT).show();
                dialog.dismiss();
                usernameEdit.setText(username);
                passwordEdit.setText("");
            } else {
                Toast.makeText(this, "用户名已存在", Toast.LENGTH_SHORT).show();
            }
        });
        
        cancelBtn.setOnClickListener(v -> dialog.dismiss());
        dialog.show();
    }
}
