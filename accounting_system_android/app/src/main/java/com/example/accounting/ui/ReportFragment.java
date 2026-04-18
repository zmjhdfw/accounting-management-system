package com.example.accounting.ui;

import android.content.Context;
import android.graphics.Color;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.Spinner;
import android.widget.TextView;
import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import com.example.accounting.R;
import com.example.accounting.data.AccountManager;
import com.example.accounting.data.VoucherManager;
import java.util.List;
import java.util.Map;
import java.util.HashMap;

/**
 * 报表查询Fragment
 */
public class ReportFragment extends Fragment {
    
    private Spinner reportTypeSpinner;
    private Button queryButton;
    private TextView reportTitle;
    private LinearLayout reportContent;
    private AccountManager accountManager;
    private VoucherManager voucherManager;
    
    private String[] reportTypes = {"科目余额表", "资产负债表", "利润表"};
    
    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater,
                            @Nullable ViewGroup container,
                            @Nullable Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_report, container, false);
        
        reportTypeSpinner = view.findViewById(R.id.report_type_spinner);
        queryButton = view.findViewById(R.id.query_button);
        reportTitle = view.findViewById(R.id.report_title);
        reportContent = view.findViewById(R.id.report_content);
        
        // 设置Spinner
        ArrayAdapter<String> adapter = new ArrayAdapter<>(requireContext(),
            android.R.layout.simple_spinner_item, reportTypes);
        adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        reportTypeSpinner.setAdapter(adapter);
        
        // 查询按钮
        queryButton.setOnClickListener(v -> generateReport());
        
        return view;
    }
    
    @Override
    public void onAttach(@NonNull Context context) {
        super.onAttach(context);
        accountManager = new AccountManager(context);
        voucherManager = new VoucherManager(context);
    }
    
    private void generateReport() {
        int position = reportTypeSpinner.getSelectedItemPosition();
        reportContent.removeAllViews();
        
        switch (position) {
            case 0:
                generateAccountBalanceReport();
                break;
            case 1:
                generateBalanceSheet();
                break;
            case 2:
                generateIncomeStatement();
                break;
        }
    }
    
    // 科目余额表
    private void generateAccountBalanceReport() {
        reportTitle.setText("科目余额表");
        
        List<AccountManager.AccountItem> accounts = accountManager.getAllAccounts();
        
        // 表头
        addTableRow("科目编码", "科目名称", "期初余额", "期末余额", true);
        
        double totalDebit = 0, totalCredit = 0;
        
        for (AccountManager.AccountItem account : accounts) {
            String balance = String.format("%.2f", account.balance);
            if (account.direction.equals("借")) {
                totalDebit += account.balance;
            } else {
                totalCredit += account.balance;
            }
            addTableRow(account.code, account.name, balance, balance, false);
        }
        
        // 合计行
        addTableRow("合计", "", 
            String.format("%.2f", totalDebit), 
            String.format("%.2f", totalCredit), true);
    }
    
    // 资产负债表
    private void generateBalanceSheet() {
        reportTitle.setText("资产负债表");
        
        List<AccountManager.AccountItem> accounts = accountManager.getAllAccounts();
        
        double assets = 0, liabilities = 0, equity = 0;
        
        for (AccountManager.AccountItem account : accounts) {
            if (account.type.equals("资产")) {
                assets += account.balance;
            } else if (account.type.equals("负债")) {
                liabilities += account.balance;
            } else if (account.type.equals("所有者权益")) {
                equity += account.balance;
            }
        }
        
        addSimpleRow("资产", String.format("%.2f", assets), true);
        addSimpleRow("负债", String.format("%.2f", liabilities), false);
        addSimpleRow("所有者权益", String.format("%.2f", equity), false);
        addSimpleRow("负债及所有者权益合计", 
            String.format("%.2f", liabilities + equity), true);
    }
    
    // 利润表
    private void generateIncomeStatement() {
        reportTitle.setText("利润表");
        
        List<AccountManager.AccountItem> accounts = accountManager.getAllAccounts();
        
        double income = 0, expense = 0;
        
        for (AccountManager.AccountItem account : accounts) {
            if (account.type.equals("收入")) {
                income += account.balance;
            } else if (account.type.equals("费用")) {
                expense += account.balance;
            }
        }
        
        double profit = income - expense;
        
        addSimpleRow("收入", String.format("%.2f", income), false);
        addSimpleRow("费用", String.format("%.2f", expense), false);
        addSimpleRow("利润", String.format("%.2f", profit), true);
    }
    
    private void addTableRow(String col1, String col2, String col3, String col4, boolean isHeader) {
        LinearLayout row = new LinearLayout(requireContext());
        row.setOrientation(LinearLayout.HORIZONTAL);
        row.setLayoutParams(new LinearLayout.LayoutParams(
            LinearLayout.LayoutParams.MATCH_PARENT,
            LinearLayout.LayoutParams.WRAP_CONTENT));
        
        if (isHeader) {
            row.setBackgroundColor(Color.parseColor("#E0E0E0"));
        }
        
        row.addView(createCell(col1, 1, isHeader));
        row.addView(createCell(col2, 2, isHeader));
        row.addView(createCell(col3, 1, isHeader));
        row.addView(createCell(col4, 1, isHeader));
        
        reportContent.addView(row);
    }
    
    private void addSimpleRow(String label, String value, boolean isBold) {
        LinearLayout row = new LinearLayout(requireContext());
        row.setOrientation(LinearLayout.HORIZONTAL);
        row.setLayoutParams(new LinearLayout.LayoutParams(
            LinearLayout.LayoutParams.MATCH_PARENT,
            LinearLayout.LayoutParams.WRAP_CONTENT));
        row.setPadding(0, 16, 0, 16);
        
        TextView labelView = new TextView(requireContext());
        labelView.setText(label);
        labelView.setTextSize(16);
        labelView.setLayoutParams(new LinearLayout.LayoutParams(0, 
            LinearLayout.LayoutParams.WRAP_CONTENT, 1));
        if (isBold) {
            labelView.setTextColor(Color.parseColor("#333333"));
            labelView.setTypeface(null, android.graphics.Typeface.BOLD);
        }
        
        TextView valueView = new TextView(requireContext());
        valueView.setText(value);
        valueView.setTextSize(16);
        valueView.setLayoutParams(new LinearLayout.LayoutParams(0, 
            LinearLayout.LayoutParams.WRAP_CONTENT, 1));
        valueView.setGravity(android.view.Gravity.END);
        if (isBold) {
            valueView.setTextColor(Color.parseColor("#333333"));
            valueView.setTypeface(null, android.graphics.Typeface.BOLD);
        }
        
        row.addView(labelView);
        row.addView(valueView);
        reportContent.addView(row);
    }
    
    private TextView createCell(String text, int weight, boolean isHeader) {
        TextView cell = new TextView(requireContext());
        cell.setText(text);
        cell.setTextSize(14);
        cell.setPadding(8, 16, 8, 16);
        cell.setLayoutParams(new LinearLayout.LayoutParams(0, 
            LinearLayout.LayoutParams.WRAP_CONTENT, weight));
        
        if (isHeader) {
            cell.setTextColor(Color.parseColor("#333333"));
            cell.setTypeface(null, android.graphics.Typeface.BOLD);
        } else {
            cell.setTextColor(Color.parseColor("#666666"));
        }
        
        return cell;
    }
}
