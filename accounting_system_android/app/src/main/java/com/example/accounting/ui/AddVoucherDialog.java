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
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;

/**
 * 添加凭证对话框
 */
public class AddVoucherDialog extends Dialog {
    
    private OnVoucherAddedListener listener;
    private EditText numberEdit;
    private EditText dateEdit;
    private EditText summaryEdit;
    private EditText debitAccountEdit;
    private EditText creditAccountEdit;
    private EditText amountEdit;
    
    public interface OnVoucherAddedListener {
        void onVoucherAdded(String number, String date, String summary, 
                          String debitAccount, String creditAccount, double amount);
    }
    
    public AddVoucherDialog(@NonNull Context context, OnVoucherAddedListener listener) {
        super(context);
        this.listener = listener;
    }
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        requestWindowFeature(Window.FEATURE_NO_TITLE);
        setContentView(R.layout.dialog_add_voucher);
        
        numberEdit = findViewById(R.id.voucher_number_edit);
        dateEdit = findViewById(R.id.voucher_date_edit);
        summaryEdit = findViewById(R.id.voucher_summary_edit);
        debitAccountEdit = findViewById(R.id.debit_account_edit);
        creditAccountEdit = findViewById(R.id.credit_account_edit);
        amountEdit = findViewById(R.id.voucher_amount_edit);
        Button saveButton = findViewById(R.id.save_button);
        Button cancelButton = findViewById(R.id.cancel_button);
        
        // 设置默认日期为今天
        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd", Locale.getDefault());
        dateEdit.setText(sdf.format(new Date()));
        
        saveButton.setOnClickListener(v -> {
            String number = numberEdit.getText().toString().trim();
            String date = dateEdit.getText().toString().trim();
            String summary = summaryEdit.getText().toString().trim();
            String debitAccount = debitAccountEdit.getText().toString().trim();
            String creditAccount = creditAccountEdit.getText().toString().trim();
            String amountStr = amountEdit.getText().toString().trim();
            
            if (number.isEmpty()) {
                Toast.makeText(getContext(), "请输入凭证号", Toast.LENGTH_SHORT).show();
                return;
            }
            
            if (date.isEmpty()) {
                Toast.makeText(getContext(), "请输入日期", Toast.LENGTH_SHORT).show();
                return;
            }
            
            if (summary.isEmpty()) {
                Toast.makeText(getContext(), "请输入摘要", Toast.LENGTH_SHORT).show();
                return;
            }
            
            if (debitAccount.isEmpty()) {
                Toast.makeText(getContext(), "请输入借方科目", Toast.LENGTH_SHORT).show();
                return;
            }
            
            if (creditAccount.isEmpty()) {
                Toast.makeText(getContext(), "请输入贷方科目", Toast.LENGTH_SHORT).show();
                return;
            }
            
            if (amountStr.isEmpty()) {
                Toast.makeText(getContext(), "请输入金额", Toast.LENGTH_SHORT).show();
                return;
            }
            
            double amount;
            try {
                amount = Double.parseDouble(amountStr);
            } catch (NumberFormatException e) {
                Toast.makeText(getContext(), "金额格式不正确", Toast.LENGTH_SHORT).show();
                return;
            }
            
            if (amount <= 0) {
                Toast.makeText(getContext(), "金额必须大于0", Toast.LENGTH_SHORT).show();
                return;
            }
            
            if (listener != null) {
                listener.onVoucherAdded(number, date, summary, debitAccount, creditAccount, amount);
            }
            dismiss();
        });
        
        cancelButton.setOnClickListener(v -> dismiss());
    }
}
