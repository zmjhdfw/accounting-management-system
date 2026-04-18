package com.example.accounting.ui;

import android.app.Dialog;
import android.content.Context;
import android.os.Bundle;
import android.view.Window;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Spinner;
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
    private EditText balanceEdit;
    private Spinner typeSpinner;
    private Spinner directionSpinner;
    
    public interface OnAccountAddedListener {
        void onAccountAdded(String code, String name, String type, double balance, String direction);
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
        balanceEdit = findViewById(R.id.account_balance_edit);
        typeSpinner = findViewById(R.id.account_type_spinner);
        directionSpinner = findViewById(R.id.account_direction_spinner);
        Button saveButton = findViewById(R.id.save_button);
        Button cancelButton = findViewById(R.id.cancel_button);
        
        // 设置科目类型下拉框
        String[] types = {"资产", "负债", "所有者权益", "收入", "费用"};
        ArrayAdapter<String> typeAdapter = new ArrayAdapter<>(getContext(),
            R.layout.spinner_item, types);
        typeAdapter.setDropDownViewResource(R.layout.spinner_dropdown_item);
        typeSpinner.setAdapter(typeAdapter);
        
        // 设置余额方向下拉框
        String[] directions = {"借", "贷"};
        ArrayAdapter<String> directionAdapter = new ArrayAdapter<>(getContext(),
            R.layout.spinner_item, directions);
        directionAdapter.setDropDownViewResource(R.layout.spinner_dropdown_item);
        directionSpinner.setAdapter(directionAdapter);
        
        saveButton.setOnClickListener(v -> {
            String code = codeEdit.getText().toString().trim();
            String name = nameEdit.getText().toString().trim();
            String balanceStr = balanceEdit.getText().toString().trim();
            String type = typeSpinner.getSelectedItem().toString();
            String direction = directionSpinner.getSelectedItem().toString();
            
            if (code.isEmpty()) {
                Toast.makeText(getContext(), "请输入科目代码", Toast.LENGTH_SHORT).show();
                return;
            }
            
            if (name.isEmpty()) {
                Toast.makeText(getContext(), "请输入科目名称", Toast.LENGTH_SHORT).show();
                return;
            }
            
            double balance = 0.0;
            if (!balanceStr.isEmpty()) {
                try {
                    balance = Double.parseDouble(balanceStr);
                } catch (NumberFormatException e) {
                    Toast.makeText(getContext(), "余额格式不正确", Toast.LENGTH_SHORT).show();
                    return;
                }
            }
            
            if (listener != null) {
                listener.onAccountAdded(code, name, type, balance, direction);
            }
            dismiss();
        });
        
        cancelButton.setOnClickListener(v -> dismiss());
    }
}
