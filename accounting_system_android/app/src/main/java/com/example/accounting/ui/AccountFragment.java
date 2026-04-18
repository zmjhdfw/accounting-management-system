package com.example.accounting.ui;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
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
    private List<String> accountList = new ArrayList<>();
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
        adapter = new AccountAdapter(accountList);
        recyclerView.setLayoutManager(new LinearLayoutManager(getContext()));
        recyclerView.setAdapter(adapter);
        
        // 添加按钮点击事件
        addButton.setOnClickListener(v -> {
            new AddAccountDialog(getContext(), (code, name) -> {
                // 添加科目到列表
                accountList.add(code + " - " + name);
                adapter.notifyDataSetChanged();
                updateView();
                Toast.makeText(getContext(), "科目添加成功", Toast.LENGTH_SHORT).show();
            }).show();
        });
        
        updateView();
        return view;
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
     * 科目列表适配器
     */
    private static class AccountAdapter extends RecyclerView.Adapter<AccountAdapter.ViewHolder> {
        private List<String> data;
        
        AccountAdapter(List<String> data) {
            this.data = data;
        }
        
        @NonNull
        @Override
        public ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
            TextView tv = new TextView(parent.getContext());
            tv.setPadding(32, 24, 32, 24);
            tv.setTextSize(16);
            return new ViewHolder(tv);
        }
        
        @Override
        public void onBindViewHolder(@NonNull ViewHolder holder, int position) {
            ((TextView) holder.itemView).setText(data.get(position));
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
