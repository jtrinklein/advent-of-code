const std = @import("std");

const Data = @This();

alloc: std.mem.Allocator,
disk_map: std.ArrayList(u8),
pub fn processInputLine(self: *Data, line: []const u8) !void {
    for (line) |c| {
        try self.disk_map.append(c - '0');
    }
}

pub fn getPart1Value(self: Data) !u64 {
    var end_i: usize = self.disk_map.items.len;
    if (@mod(end_i, 2) == 1) {
        end_i -= 1;
    }
    var total: u64 = 0;
    var checksum_idx: usize = 0;
    var done = false;
    var files = try self.disk_map.clone();
    defer files.deinit();

    for (files.items, 0..) |d, i| {
        const is_even_idx = @mod(i, 2) == 0;
        var file_idx = if (is_even_idx) @divFloor(i, 2) else @divFloor(end_i, 2);

        for (0..d) |_| {
            if (end_i < i) {
                done = true;
                break;
            }

            total += checksum_idx * file_idx;
            if (!is_even_idx) {
                files.items[end_i] -= 1;
                if (files.items[end_i] == 0) {
                    end_i -= 2;
                    file_idx = @divFloor(end_i, 2);
                }
            }
            checksum_idx += 1;
        }
        if (done) {
            break;
        }
    }
    return total;
}

pub fn getPart2Value(self: Data) !u64 {
    var file_ids = std.ArrayList(usize).init(self.alloc);
    defer file_ids.deinit();
    var file_sizes = try self.disk_map.clone();
    defer file_sizes.deinit();

    // make sure end_i is even
    var end_i: usize = if (@mod(file_sizes.items.len - 1, 2) == 0) file_sizes.items.len - 1 else file_sizes.items.len - 2;
    const invalid_id = @divFloor(end_i, 2) + 1;

    for (0..file_sizes.items.len) |fi| {
        if (@mod(fi, 2) == 0) {
            try file_ids.append(@divFloor(fi, 2));
        } else {
            try file_ids.append(invalid_id);
        }
    }
    var i: usize = 0;
    while (i < end_i) {
        const idx = end_i - i;

        var go_next = true;
        const current_size = file_sizes.items[idx];
        const current_id = file_ids.items[idx];
        if (current_id == invalid_id) {
            i += 1;
            continue;
        }
        for (1..idx) |j| {
            if (file_ids.items[j] == invalid_id and file_sizes.items[j] >= current_size) {
                file_ids.items[idx] = invalid_id;
                if (current_size == file_sizes.items[j]) {
                    file_ids.items[j] = current_id;
                } else {
                    const new_empty_size = file_sizes.items[j] - current_size;
                    file_sizes.items[j] = new_empty_size;
                    try file_sizes.insert(j, current_size);
                    try file_ids.insert(j, current_id);
                    end_i += 1;
                    go_next = false;
                }
                break;
            }
        }
        if (go_next) {
            i += 1;
        }
    }

    var total: u64 = 0;
    var checksum_idx: usize = 0;

    for (file_ids.items, 0..) |fid, j| {
        const size = file_sizes.items[j];
        if (fid == invalid_id) {
            checksum_idx += size;
        } else {
            for (0..size) |_| {
                total += fid * checksum_idx;
                checksum_idx += 1;
            }
        }
    }
    return total;
}
pub fn init(alloc: std.mem.Allocator) Data {
    return .{
        .alloc = alloc,
        .disk_map = std.ArrayList(u8).init(alloc),
    };
}

pub fn deinit(self: Data) void {
    self.disk_map.deinit();
}
