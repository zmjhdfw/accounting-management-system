package com.example.accounting.data;

import android.content.Context;
import android.content.SharedPreferences;
import java.util.ArrayList;
import java.util.List;

/**
 * 凭证管理类
 */
public class VoucherManager {
    private static final String PREF_NAME = "voucher_prefs";
    private static final String KEY_VOUCHERS = "vouchers";
    
    private SharedPreferences prefs;
    
    public VoucherManager(Context context) {
        prefs = context.getSharedPreferences(PREF_NAME, Context.MODE_PRIVATE);
    }
    
    // 凭证数据类
    public static class VoucherItem {
        public String number;
        public String date;
        public String summary;
        public String debitAccount;
        public String creditAccount;
        public double amount;
        
        public VoucherItem(String number, String date, String summary, 
                          String debitAccount, String creditAccount, double amount) {
            this.number = number;
            this.date = date;
            this.summary = summary;
            this.debitAccount = debitAccount;
            this.creditAccount = creditAccount;
            this.amount = amount;
        }
        
        @Override
        public String toString() {
            return number + ":" + date + ":" + summary + ":" + 
                   debitAccount + ":" + creditAccount + ":" + amount;
        }
        
        public static VoucherItem fromString(String str) {
            String[] parts = str.split(":");
            if (parts.length >= 6) {
                return new VoucherItem(
                    parts[0],
                    parts[1],
                    parts[2],
                    parts[3],
                    parts[4],
                    Double.parseDouble(parts[5])
                );
            }
            return null;
        }
    }
    
    // 获取所有凭证
    public List<VoucherItem> getAllVouchers() {
        List<VoucherItem> vouchers = new ArrayList<>();
        String vouchersStr = prefs.getString(KEY_VOUCHERS, "");
        if (!vouchersStr.isEmpty()) {
            for (String voucherStr : vouchersStr.split(";")) {
                VoucherItem voucher = VoucherItem.fromString(voucherStr);
                if (voucher != null) vouchers.add(voucher);
            }
        }
        return vouchers;
    }
    
    // 保存所有凭证
    private void saveAllVouchers(List<VoucherItem> vouchers) {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < vouchers.size(); i++) {
            if (i > 0) sb.append(";");
            sb.append(vouchers.get(i).toString());
        }
        prefs.edit().putString(KEY_VOUCHERS, sb.toString()).apply();
    }
    
    // 添加凭证
    public boolean addVoucher(VoucherItem voucher) {
        List<VoucherItem> vouchers = getAllVouchers();
        vouchers.add(voucher);
        saveAllVouchers(vouchers);
        return true;
    }
    
    // 更新凭证
    public boolean updateVoucher(int index, VoucherItem voucher) {
        List<VoucherItem> vouchers = getAllVouchers();
        if (index >= 0 && index < vouchers.size()) {
            vouchers.set(index, voucher);
            saveAllVouchers(vouchers);
            return true;
        }
        return false;
    }
    
    // 删除凭证
    public boolean deleteVoucher(int index) {
        List<VoucherItem> vouchers = getAllVouchers();
        if (index >= 0 && index < vouchers.size()) {
            vouchers.remove(index);
            saveAllVouchers(vouchers);
            return true;
        }
        return false;
    }
    
    // 获取下一个凭证号
    public String getNextVoucherNumber() {
        List<VoucherItem> vouchers = getAllVouchers();
        if (vouchers.isEmpty()) {
            return "001";
        }
        try {
            int max = 0;
            for (VoucherItem v : vouchers) {
                int num = Integer.parseInt(v.number);
                if (num > max) max = num;
            }
            return String.format("%03d", max + 1);
        } catch (Exception e) {
            return String.format("%03d", vouchers.size() + 1);
        }
    }
}
