package com.example.accounting.ui;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Spinner;
import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import com.example.accounting.R;

/**
 * 报表查询Fragment
 */
public class ReportFragment extends Fragment {
    
    private Spinner reportTypeSpinner;
    
    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater,
                            @Nullable ViewGroup container,
                            @Nullable Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_report, container, false);
        
        reportTypeSpinner = view.findViewById(R.id.report_type_spinner);
        
        // TODO: 设置报表类型和查询逻辑
        
        return view;
    }
}
