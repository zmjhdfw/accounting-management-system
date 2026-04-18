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
import androidx.recyclerview.widget.RecyclerView;
import com.example.accounting.R;

/**
 * 科目管理Fragment
 */
public class AccountFragment extends Fragment {
    
    private RecyclerView recyclerView;
    private TextView emptyView;
    private Button addButton;
    
    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, 
                            @Nullable ViewGroup container,
                            @Nullable Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_account, container, false);
        
        recyclerView = view.findViewById(R.id.account_recycler_view);
        emptyView = view.findViewById(R.id.empty_view);
        addButton = view.findViewById(R.id.add_account_button);
        
        // 显示空状态提示
        if (emptyView != null) {
            emptyView.setText("暂无科目数据\n\n点击上方\"添加科目\"按钮添加\n\n示例科目：\n• 1001 库存现金\n• 1002 银行存款\n• 1101 短期投资");
            emptyView.setVisibility(View.VISIBLE);
        }
        
        // 添加按钮点击事件
        if (addButton != null) {
            addButton.setOnClickListener(v -> {
                Toast.makeText(getContext(), "添加科目功能开发中...", Toast.LENGTH_SHORT).show();
            });
        }
        
        return view;
    }
}
