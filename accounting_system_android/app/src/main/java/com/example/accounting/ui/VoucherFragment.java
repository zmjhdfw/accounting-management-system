package com.example.accounting.ui;

import android.app.AlertDialog;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;
import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;
import com.example.accounting.R;
import java.util.ArrayList;
import java.util.List;

/**
 * 凭证管理Fragment
 */
public class VoucherFragment extends Fragment {
    
    private RecyclerView recyclerView;
    private TextView emptyView;
    private Button addButton;
    private List<VoucherItem> voucherList = new ArrayList<>();
    private VoucherAdapter adapter;
    
    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater,
                            @Nullable ViewGroup container,
                            @Nullable Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_voucher, container, false);
        
        recyclerView = view.findViewById(R.id.voucher_recycler_view);
        emptyView = view.findViewById(R.id.empty_view);
        addButton = view.findViewById(R.id.add_voucher_button);
        
        // 设置RecyclerView
        adapter = new VoucherAdapter(voucherList, this);
        recyclerView.setLayoutManager(new LinearLayoutManager(getContext()));
        recyclerView.setAdapter(adapter);
        
        // 添加按钮点击事件
        addButton.setOnClickListener(v -> showAddDialog());
        
        updateView();
        return view;
    }
    
    private void showAddDialog() {
        new AddVoucherDialog(getContext(), (number, date, summary, debitAccount, creditAccount, amount) -> {
            // 添加凭证到列表
            voucherList.add(new VoucherItem(number, date, summary, debitAccount, creditAccount, amount));
            adapter.notifyDataSetChanged();
            updateView();
            Toast.makeText(getContext(), "凭证添加成功", Toast.LENGTH_SHORT).show();
        }).show();
    }
    
    private void showEditDialog(int position) {
        VoucherItem item = voucherList.get(position);
        AddVoucherDialog dialog = new AddVoucherDialog(getContext(), 
            (number, date, summary, debitAccount, creditAccount, amount) -> {
                item.number = number;
                item.date = date;
                item.summary = summary;
                item.debitAccount = debitAccount;
                item.creditAccount = creditAccount;
                item.amount = amount;
                adapter.notifyDataSetChanged();
                Toast.makeText(getContext(), "凭证修改成功", Toast.LENGTH_SHORT).show();
            });
        dialog.show();
        // 预填充数据
        dialog.findViewById(R.id.voucher_number_edit).post(() -> {
            EditText numberEdit = dialog.findViewById(R.id.voucher_number_edit);
            EditText dateEdit = dialog.findViewById(R.id.voucher_date_edit);
            EditText summaryEdit = dialog.findViewById(R.id.voucher_summary_edit);
            EditText debitEdit = dialog.findViewById(R.id.debit_account_edit);
            EditText creditEdit = dialog.findViewById(R.id.credit_account_edit);
            EditText amountEdit = dialog.findViewById(R.id.voucher_amount_edit);
            
            numberEdit.setText(item.number);
            dateEdit.setText(item.date);
            summaryEdit.setText(item.summary);
            debitEdit.setText(item.debitAccount);
            creditEdit.setText(item.creditAccount);
            // 格式化金额
            if (item.amount == (long) item.amount) {
                amountEdit.setText(String.format("%.0f", item.amount));
            } else {
                amountEdit.setText(String.format("%.2f", item.amount));
            }
        });
    }
    
    private void deleteVoucher(int position) {
        new AlertDialog.Builder(getContext())
            .setTitle("确认删除")
            .setMessage("确定要删除凭证 " + voucherList.get(position).number + " 吗？")
            .setPositiveButton("删除", (d, w) -> {
                voucherList.remove(position);
                adapter.notifyDataSetChanged();
                updateView();
                Toast.makeText(getContext(), "凭证已删除", Toast.LENGTH_SHORT).show();
            })
            .setNegativeButton("取消", null)
            .show();
    }
    
    private void updateView() {
        if (voucherList.isEmpty()) {
            emptyView.setVisibility(View.VISIBLE);
            recyclerView.setVisibility(View.GONE);
            emptyView.setText("暂无凭证数据\n\n点击上方\"添加凭证\"按钮添加\n\n凭证格式：\n• 凭证号\n• 日期\n• 摘要\n• 借方科目\n• 贷方科目\n• 金额");
        } else {
            emptyView.setVisibility(View.GONE);
            recyclerView.setVisibility(View.VISIBLE);
        }
    }
    
    /**
     * 凭证数据类
     */
    static class VoucherItem {
        String number;          // 凭证号
        String date;            // 日期
        String summary;         // 摘要
        String debitAccount;    // 借方科目
        String creditAccount;   // 贷方科目
        double amount;          // 金额
        
        VoucherItem(String number, String date, String summary, 
                   String debitAccount, String creditAccount, double amount) {
            this.number = number;
            this.date = date;
            this.summary = summary;
            this.debitAccount = debitAccount;
            this.creditAccount = creditAccount;
            this.amount = amount;
        }
    }
    
    /**
     * 凭证列表适配器
     */
    private static class VoucherAdapter extends RecyclerView.Adapter<VoucherAdapter.ViewHolder> {
        private List<VoucherItem> data;
        private VoucherFragment fragment;
        
        VoucherAdapter(List<VoucherItem> data, VoucherFragment fragment) {
            this.data = data;
            this.fragment = fragment;
        }
        
        @NonNull
        @Override
        public ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
            View view = LayoutInflater.from(parent.getContext())
                .inflate(android.R.layout.simple_list_item_2, parent, false);
            return new ViewHolder(view);
        }
        
        @Override
        public void onBindViewHolder(@NonNull ViewHolder holder, int position) {
            VoucherItem item = data.get(position);
            TextView text1 = holder.itemView.findViewById(android.R.id.text1);
            TextView text2 = holder.itemView.findViewById(android.R.id.text2);
            
            // 第一行：凭证号、日期、摘要
            text1.setText(String.format("凭证%s | %s | %s", item.number, item.date, item.summary));
            text1.setTextSize(14);
            text1.setTextColor(0xFF000000);
            
            // 第二行：借方、贷方、金额
            text2.setText(String.format("借:%s 贷:%s 金额:%.2f", 
                item.debitAccount, item.creditAccount, item.amount));
            text2.setTextSize(12);
            text2.setTextColor(0xFF666666);
            
            // 点击编辑
            holder.itemView.setOnClickListener(v -> fragment.showEditDialog(position));
            
            // 长按删除
            holder.itemView.setOnLongClickListener(v -> {
                fragment.deleteVoucher(position);
                return true;
            });
        }
        
        @Override
        public int getItemCount() {
            return data.size();
        }
        
        static class ViewHolder extends RecyclerView.ViewHolder {
            ViewHolder(View itemView) {
                super(itemView);
            }
        }
    }
}
