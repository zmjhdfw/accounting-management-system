package com.example.accounting.ui;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
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
    
    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, 
                            @Nullable ViewGroup container,
                            @Nullable Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_account, container, false);
        
        recyclerView = view.findViewById(R.id.account_recycler_view);
        
        // TODO: 设置适配器和加载数据
        
        return view;
    }
}
