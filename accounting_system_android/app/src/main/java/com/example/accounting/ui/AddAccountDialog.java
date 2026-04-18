package com.example.accounting.ui;

import android.app.Dialog;
import android.content.Context;
import android.os.Bundle;
import android.view.Window;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;
import androidx.annotation.NonNull;
import com.example.accounting.R;

/**
 * 添加科目对话框
 */
public class AddAccountDialog extends Dialog {
    
    private OnAccountAddedListener listener;
    private EditText codeEdit;
    private EditText nameEdit;
    
    public interface OnAccountAddedListener {
        void onAccountAdded(String code, String name);
    }
    
    public AddAccountDialog(@NonNull Context context, OnAccountAddedListener listener) {
        super(context);
        this.listener = listener;
    }
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        requestWindowFeature(Window.FEATURE_NO_TITLE);
        setContentView(R.layout.dialog_add_account);
        
        codeEdit = findViewById(R.id.account_code_edit);
        nameEdit = findViewById(R.id.account_name_edit);
        Button saveButton = findViewById(R.id.save_button);
        Button cancelButton = findViewById(R.id.cancel_button);
        
        saveButton.setOnClickListener(v -> {
            String code = codeEdit.getText().toString().trim();
            String name = nameEdit.getText().toString().trim();
            
            if (code.isEmpty()) {
                Toast.makeText(getContext(), "请输入科目代码", Toast.LENGTH_SHORT).show();
                return;
            }
            
            if (name.isEmpty()) {
                Toast.makeText(getContext(), "请输入科目名称", Toast.LENGTH_SHORT).show();
                return;
            }
            
            if (listener != null) {
                listener.onAccountAdded(code, name);
            }
            dismiss();
        });
        
        cancelButton.setOnClickListener(v -> dismiss());
    }
}
