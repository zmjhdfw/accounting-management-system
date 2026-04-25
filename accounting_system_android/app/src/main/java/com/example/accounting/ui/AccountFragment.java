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
import androidx.lifecycle.ViewModelProvider;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;
import com.example.accounting.R;
import com.example.accounting.data.model.AccountItem;
import com.example.accounting.ui.viewmodel.AccountViewModel;
import java.util.ArrayList;
import java.util.List;

/**
 * 科目管理Fragment
 * 使用ViewModel管理数据，观察LiveData自动更新UI，确保数据持久化
 */
public class AccountFragment extends Fragment {
    
    private RecyclerView recyclerView;
    private TextView emptyView;
    private Button addButton;
    private AccountViewModel viewModel;
    private AccountAdapter adapter;
    
    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, 
                            @Nullable ViewGroup container,
                            @Nullable Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_account, container, false);
        
        recyclerView = view.findViewById(R.id.account_recycler_view);
        emptyView = view.findViewById(R.id.empty_view);
        addButton = view.findViewById(R.id.add_account_button);
        
        // 设置RecyclerView
        adapter = new AccountAdapter(this);
        recyclerView.setLayoutManager(new LinearLayoutManager(getContext()));
        recyclerView.setAdapter(adapter);
        
        // 添加按钮点击事件
        addButton.setOnClickListener(v -> showAddDialog());
        
        return view;
    }
    
    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);
        
        // 初始化ViewModel
        viewModel = new ViewModelProvider(this).get(AccountViewModel.class);
        
        // 观察科目数据
        viewModel.getAccounts().observe(getViewLifecycleOwner(), accounts -> {
            adapter.setData(accounts);
            updateView();
        });
        
        // 观察错误消息
        viewModel.getErrorMessage().observe(getViewLifecycleOwner(), message -> {
            if (message != null && !message.isEmpty()) {
                Toast.makeText(getContext(), message, Toast.LENGTH_SHORT).show();
            }
        });
    }
    
    private void showAddDialog() {
        new AddAccountDialog(getContext(), (code, name, type, balance, direction) -> {
            AccountItem account = new AccountItem(code, name, type, balance, direction);
            viewModel.addAccount(account);
            Toast.makeText(getContext(), "科目添加成功", Toast.LENGTH_SHORT).show();
        }).show();
    }
    
    private void showEditDialog(int position) {
        AccountItem item = adapter.getItem(position);
        AddAccountDialog dialog = new AddAccountDialog(getContext(), (code, name, type, balance, direction) -> {
            AccountItem updated = new AccountItem(code, name, type, balance, direction);
            viewModel.updateAccount(updated);
            Toast.makeText(getContext(), "科目修改成功", Toast.LENGTH_SHORT).show();
        });
        dialog.show();
        // 预填充数据
        dialog.findViewById(R.id.account_code_edit).post(() -> {
            EditText codeEdit = dialog.findViewById(R.id.account_code_edit);
            EditText nameEdit = dialog.findViewById(R.id.account_name_edit);
            EditText balanceEdit = dialog.findViewById(R.id.account_balance_edit);
            codeEdit.setText(item.getCode());
            nameEdit.setText(item.getName());
            // 格式化余额，避免科学计数法
            if (item.getBalance() == (long) item.getBalance()) {
                balanceEdit.setText(String.format("%.0f", item.getBalance()));
            } else {
                balanceEdit.setText(String.format("%.2f", item.getBalance()));
            }
        });
    }
    
    private void deleteAccount(int position) {
        AccountItem item = adapter.getItem(position);
        new AlertDialog.Builder(getContext())
            .setTitle("确认删除")
            .setMessage("确定要删除科目 " + item.getCode() + " 吗？")
            .setPositiveButton("删除", (d, w) -> {
                viewModel.deleteAccount(item.getCode());
                Toast.makeText(getContext(), "科目已删除", Toast.LENGTH_SHORT).show();
            })
            .setNegativeButton("取消", null)
            .show();
    }
    
    private void updateView() {
        if (adapter.getItemCount() == 0) {
            emptyView.setVisibility(View.VISIBLE);
            recyclerView.setVisibility(View.GONE);
            emptyView.setText("暂无科目数据\n\n点击上方\"添加科目\"按钮添加\n\n示例科目：\n• 1001 库存现金\n• 1002 银行存款\n• 1101 短期投资");
        } else {
            emptyView.setVisibility(View.GONE);
            recyclerView.setVisibility(View.VISIBLE);
        }
    }
    
    /**
     * 科目列表适配器
     */
    private static class AccountAdapter extends RecyclerView.Adapter<AccountAdapter.ViewHolder> {
        private List<AccountItem> data = new ArrayList<>();
        private AccountFragment fragment;
        
        AccountAdapter(AccountFragment fragment) {
            this.fragment = fragment;
        }
        
        /**
         * 设置数据
         */
        public void setData(List<AccountItem> newData) {
            this.data = newData != null ? newData : new ArrayList<>();
            notifyDataSetChanged();
        }
        
        /**
         * 获取指定位置的数据项
         */
        public AccountItem getItem(int position) {
            return data.get(position);
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
            AccountItem item = data.get(position);
            TextView text1 = holder.itemView.findViewById(android.R.id.text1);
            TextView text2 = holder.itemView.findViewById(android.R.id.text2);
            
            // 第一行：科目代码和名称
            text1.setText(item.getCode() + " - " + item.getName());
            text1.setTextSize(16);
            text1.setTextColor(0xFF000000);
            
            // 第二行：类型、余额、方向
            text2.setText(String.format("类型: %s | 余额: %.2f | 方向: %s", 
                item.getType(), item.getBalance(), item.getDirection()));
            text2.setTextSize(12);
            text2.setTextColor(0xFF666666);
            
            // 点击编辑
            holder.itemView.setOnClickListener(v -> fragment.showEditDialog(position));
            
            // 长按删除
            holder.itemView.setOnLongClickListener(v -> {
                fragment.deleteAccount(position);
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
