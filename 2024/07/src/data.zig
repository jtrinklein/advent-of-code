const std = @import("std");

const Data = @This();

alloc: std.mem.Allocator,
equations: std.ArrayList(std.ArrayList(i64)),
test_vals: std.ArrayList(i64),
ops: std.ArrayList(u8),

pub fn processInputLine(self: *Data, line: []const u8) !void {
    var it = std.mem.splitAny(u8, line, ": ");
    const tval = it.first();
    try self.test_vals.append(try std.fmt.parseInt(i64, tval, 10));
    var eq = std.ArrayList(i64).init(self.alloc);
    errdefer eq.deinit();
    while (it.next()) |val| {
        if (val.len == 0) continue;
        try eq.append(try std.fmt.parseInt(i64, val, 10));
    }
    try self.equations.append(eq);
    // print("\neq.items.len: {d}\n", .{eq.items.len});

    const op_count: u8 = @intCast(eq.items.len - 1);
    // print("op_count : {d}\n", .{op_count});
    try self.ops.append(op_count);
}
fn println(comptime str: []const u8, args: anytype) void {
    std.debug.print(str, args);
    std.debug.print("\n", .{});
}
fn printlnif(total: i64, match: i64, comptime str: []const u8, args: anytype) void {
    if (total == match) {
        println(str, args);
    }
}
const print = std.debug.print;

fn is_bit_set(bit: u6, value: u64) bool {
    return value & (@as(u64, 1) << bit ) != 0;
}
pub fn getPart1Value(self: Data) !i64 {
    var calibration_result: i64 = 0;
    for (self.test_vals.items, 0..) |total, i| {
        const op_combinations: usize = std.math.pow(usize, 2, self.ops.items[i]);
        var solved = false;
        for (0..op_combinations+1) |op_selector| {
            if (solved) {
                break;
            }
            var calc: i64 = 0;
            var op_index: u6 = 0;
            for (self.equations.items[i].items) |eq| {
                if (calc == 0) {
                    calc = eq;
                    continue;
                }
                defer op_index += 1;
                if (is_bit_set(op_index, op_selector)) {
                    calc *= eq;
                } else {
                    calc += eq;
                }
                
                if (calc > total) {
                    break;
                }
            }
            
            if (calc == total) {
                solved = true;
                break;
            }
        } 
        if (solved) {
            calibration_result += total;
        }
    }
    return calibration_result;
}
pub fn getPart2Value(self: *Data) !i64 {
    var success: usize = 0;
    var calibration_result: i64 = 0;
    var failed_indicies = std.ArrayList(usize).init(self.alloc);
    defer failed_indicies.deinit();
    for (self.test_vals.items, 0..) |total, i| {
        const op_combinations: usize = std.math.pow(usize, 2, self.ops.items[i]);
        var solved = false;
        for (0..op_combinations) |op_selector| {
            if (solved) {
                break;
            }
            var calc: i64 = 0;
            var op_index: u6 = 0;
            for (self.equations.items[i].items) |eq| {
                if (calc == 0) {
                    calc = eq;
                    continue;
                }
                defer op_index += 1;
                if (is_bit_set(op_index, op_selector)) {
                    calc *= eq;
                } else {
                    calc += eq;
                }
                
                if (calc > total) {
                    break;
                }
            }
            
            if (calc == total) {
                solved = true;
                break;
            }
        } 
        if (solved) {
            calibration_result += total;
            success += 1;
        }else {
            try failed_indicies.append(i);
        }
    }
    print("{d} / {d} succeeded\n{d} failed\n\npart1: {d}\n\n",.{success, self.equations.items.len, failed_indicies.items.len, calibration_result});
    // const concat_results = try self.getValueWithConcat(failed_indicies);
    const concat_results = try self.getValueRtlTest(failed_indicies);
    print("what result?? {d}", .{concat_results});
    return calibration_result + concat_results;
}

fn mergeNumbers(lhs: i64, rhs: i64) i64 {
    var mult: i64 = 1;
    while (@mod(rhs, mult) != rhs) {
        mult *= 10;
    }
    return lhs * 10 + rhs;
}

fn getMultMask(lhs: i64, rhs: i64) i64 {
    const smaller = if (lhs < rhs) lhs else rhs;
    var mult: i64 = 10;
    while(@mod(smaller, mult) != smaller) {
        mult *= 10;
    }
    return mult;
}
fn numberEndsWithNumber(larger: i64, smaller: i64, mult_mask: i64) bool {
    const r = @mod(larger, mult_mask);
    const match = r == smaller;
    // println("\n{d} end with {d} ? {d} == {d} -> {any}", .{larger, smaller, r, smaller, match });
    return match;
}

const Op = enum {
    Mult,
    Add,
    Concat,
    Nop
};


fn getValueRtlTest(self: Data, failed_indicies: std.ArrayList(usize)) ! i64 {
    var retval: i64 = 0;
    const log_total: i64 = 7290;
    for (failed_indicies.items) |failed_idx| {
        const total = self.test_vals.items[failed_idx];
        const eq: std.ArrayList(i64) = self.equations.items[failed_idx];
        // TODO: actually set ops flags by determining ALL possilbe operators for each position
        const ops = try self.alloc.alloc(u3,self.ops.items[failed_idx]);
        defer self.alloc.free(ops);

        var value = total;
        var success = true;
        printlnif(total, log_total,"for total: {d}", .{total});
        for (0..eq.items.len) | i| {
            
            const eq_i = eq.items.len - i - 1;
            const eq_value = eq.items[eq_i];
            printlnif(total, log_total,"{d}: v: {d} eqv: {d} ", .{i, value, eq_value});
            if (value <= 0) {
                printlnif(total, log_total,"value is less or 0", .{});
                success = false;
                break;
            }
            if (value == eq_value) {
                printlnif(total, log_total,"value matches", .{});
                value -= eq_value;
                continue;
            }
            const mult_mask = getMultMask(value, eq_value);
            printlnif(total, log_total," mask {d} ", .{mult_mask});
            if (@mod(value, eq_value) == 0) {
                // undo *
                printlnif(total, log_total,"undo mult", .{});
                value = @divFloor(value, eq_value);
            } else if (numberEndsWithNumber(value, eq_value, mult_mask)) {
                // undo ||
                printlnif(total, log_total,"undo concat", .{});
                value = @divFloor(value - eq_value, mult_mask);
            } else  {
                // undo +
                printlnif(total, log_total,"undo add", .{});
                value -= eq_value;
            }
            printlnif(total, log_total, "new value: {d}\n-------------------", .{value});
        }
        success = success and value == 0;
        if (success) {
            retval += total;
            println("succeeded total: {d} -> {d}", .{total, retval});
        } else {
            println("failed total: {d}", .{total});
        }
    }
    return retval;
}

fn getValueWithConcat(self: *Data, failed_indicies: std.ArrayList(usize)) !i64 {
    var calibration_result: i64 = 0;
    var success: usize = 0;
    
    for (failed_indicies.items) | i| {
        const total = self.test_vals.items[i];
        print("failed: {d}: {any}\n", .{total, self.equations.items[i].items});
        const op_combinations: u64 = std.math.pow(u64, 3, self.ops.items[i]);
        var solved = false;
        var op_combo_i: u64 = 0;
        var current_ops = try self.alloc.alloc(u2, op_combinations);
        defer self.alloc.free(current_ops);
        @memset(current_ops, 0);

        //update ops
        while (op_combo_i < op_combinations) {
            defer op_combo_i += 1;

            var op_i: usize = 0;
            var calc: i64 = 0;
            for (self.equations.items[i].items) |eq| {
                if (calc == 0) {
                    calc = eq;
                    continue;
                }
                defer op_i += 1;
                switch(current_ops[op_i]) {
                    0 => {
                        calc = mergeNumbers(calc, eq);
                    },
                    1 => {
                        calc += eq;
                    },
                    2 => {
                        calc *= eq;
                    },
                    else => {},
                }
                
                if (calc > total) {
                    break;
                }
            }
            
            if (calc == total) {
                solved = true;
                break;
            }
        
            op_i = 0;    
            while (op_i < current_ops.len) {
                current_ops[op_i] = @mod(current_ops[op_i] + 1, 3);
                if (current_ops[op_i] == 0) {
                    op_i += 1;
                } else {
                    op_i = current_ops.len;
                }
            }
        } 
        if (solved) {
            print("  - success\n", .{});
            calibration_result += total;
            success += 1;
        } else {
            
            print("  - failed\n", .{});
        }
    }
    print("{d} / {d} success\n",.{success, failed_indicies.items.len});
    return calibration_result;
}

pub fn init(alloc: std.mem.Allocator) Data {
    const equations = std.ArrayList(std.ArrayList(i64)).init(alloc);
    errdefer equations.deinit();
    const test_vals = std.ArrayList(i64).init(alloc);
    errdefer test_vals.deinit();
    const ops = std.ArrayList(u8).init(alloc);
    return .{
        .alloc = alloc,
        .equations = equations,
        .test_vals = test_vals,
        .ops = ops,
    };
}

pub fn deinit(self: Data) void {
    for (self.equations.items) |eq| {
        eq.deinit();
    }
    self.equations.deinit();
    self.test_vals.deinit();
    self.ops.deinit();
}
