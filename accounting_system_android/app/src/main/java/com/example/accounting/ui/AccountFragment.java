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
 * 科目管理Fragment
 */
public class AccountFragment extends Fragment {
    
    private RecyclerView recyclerView;
    private TextView emptyView;
    private Button addButton;
    private List<AccountItem> accountList = new ArrayList<>();
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
        adapter = new AccountAdapter(accountList, this);
        recyclerView.setLayoutManager(new LinearLayoutManager(getContext()));
        recyclerView.setAdapter(adapter);
        
        // 添加按钮点击事件
        addButton.setOnClickListener(v -> showAddDialog());
        
        updateView();
        return view;
    }
    
    private void showAddDialog() {
        new AddAccountDialog(getContext(), (code, name) -> {
            // 添加科目到列表
            accountList.add(new AccountItem(code, name));
            adapter.notifyDataSetChanged();
            updateView();
            Toast.makeText(getContext(), "科目添加成功", Toast.LENGTH_SHORT).show();
        }).show();
    }
    
    private void showEditDialog(int position) {
        AccountItem item = accountList.get(position);
        AddAccountDialog dialog = new AddAccountDialog(getContext(), (code, name) -> {
            item.code = code;
            item.name = name;
            adapter.notifyDataSetChanged();
            Toast.makeText(getContext(), "科目修改成功", Toast.LENGTH_SHORT).show();
        });
        dialog.show();
        // 预填充数据
        dialog.findViewById(R.id.account_code_edit).post(() -> {
            EditText codeEdit = dialog.findViewById(R.id.account_code_edit);
            EditText nameEdit = dialog.findViewById(R.id.account_name_edit);
            codeEdit.setText(item.code);
            nameEdit.setText(item.name);
        });
    }
    
    private void deleteAccount(int position) {
        new AlertDialog.Builder(getContext())
            .setTitle("确认删除")
            .setMessage("确定要删除科目 " + accountList.get(position).code + " 吗？")
            .setPositiveButton("删除", (d, w) -> {
                accountList.remove(position);
                adapter.notifyDataSetChanged();
                updateView();
                Toast.makeText(getContext(), "科目已删除", Toast.LENGTH_SHORT).show();
            })
            .setNegativeButton("取消", null)
            .show();
    }
    
    private void updateView() {
        if (accountList.isEmpty()) {
            emptyView.setVisibility(View.VISIBLE);
            recyclerView.setVisibility(View.GONE);
            emptyView.setText("暂无科目数据\n\n点击上方\"添加科目\"按钮添加\n\n示例科目：\n• 1001 库存现金\n• 1002 银行存款\n• 1101 短期投资");
        } else {
            emptyView.setVisibility(View.GONE);
            recyclerView.setVisibility(View.VISIBLE);
        }
    }
    
    /**
     * 科目数据类
     */
    static class AccountItem {
        String code;
        String name;
        
        AccountItem(String code, String name) {
            this.code = code;
            this.name = name;
        }
    }
    
    /**
     * 科目列表适配器
     */
    private static class AccountAdapter extends RecyclerView.Adapter<AccountAdapter.ViewHolder> {
        private List<AccountItem> data;
        private AccountFragment fragment;
        
        AccountAdapter(List<AccountItem> data, AccountFragment fragment) {
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
            AccountItem item = data.get(position);
            TextView text1 = holder.itemView.findViewById(android.R.id.text1);
            TextView text2 = holder.itemView.findViewById(android.R.id.text2);
            text1.setText(item.code + " - " + item.name);
            text2.setText("点击编辑 | 长按删除");
            text1.setTextSize(16);
            text2.setTextSize(12);
            
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
