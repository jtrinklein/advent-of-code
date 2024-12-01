const std = @import("std");

const Data = struct {
    lefts: std.ArrayList(i32),
    rights: std.ArrayList(i32),
    pub fn deinit(self: Data) void {
        self.lefts.deinit();
        self.rights.deinit();
    }
};
fn readData(alloc: std.mem.Allocator) !Data {
    var file = try std.fs.cwd().openFile("data.txt", .{});
    defer file.close();

    var buf_read = std.io.bufferedReader(file.reader());
    var in_stream = buf_read.reader();
    var buf: [1024]u8 = undefined;

    var lefts = std.ArrayList(i32).init(alloc);
    errdefer lefts.deinit();

    var rights = std.ArrayList(i32).init(alloc);
    errdefer rights.deinit();

    while (try in_stream.readUntilDelimiterOrEof(&buf, '\n')) |line| {
        const trimmed = if (@import("builtin").os.tag == .windows) std.mem.trimRight(u8, line, "\r") else line;
        var it = std.mem.splitSequence(u8, trimmed, "   ");
        if (it.next()) |l| {
            try lefts.append(try std.fmt.parseInt(i32, l, 10));
        }
        if (it.next()) |r| {
            try rights.append(try std.fmt.parseInt(i32, r, 10));
        }
    }
    const data: Data = .{
        .lefts = lefts,
        .rights = rights,
    };
    sortData(data);
    return data;
}

fn sortData(data: Data) void {
    std.mem.sort(i32, data.lefts.items, {}, std.sort.asc(i32));
    std.mem.sort(i32, data.rights.items, {}, std.sort.asc(i32));
}

fn part1(data: Data) !u32 {
    var total: u32 = 0;
    for (data.lefts.items, data.rights.items) |left, right| {
        total += @abs(right - left);
    }
    return total;
}

fn part2(data: Data) !u32 {
    var sim_score: u32 = 0;
    var last: i32 = -1;
    var count: u32 = 0;
    var r_start: usize = 0;
    for (data.lefts.items) |n| {
        if (n == last) {
            const score = count * @as(u32, @intCast(n));
            sim_score += score;
            continue;
        }
        count = 0;

        for (data.rights.items[r_start..]) |r| {
            if (r == n) {
                count += 1;
            }
            if (r > n) {
                break;
            }
        }
        const otherscore = count * @as(u32, @intCast(n));
        sim_score += otherscore;
        r_start += count;
        last = n;
    }

    return sim_score;
}
pub fn main() !void {
    // Prints to stderr (it's a shortcut based on `std.io.getStdErr()`)
    std.debug.print("All your {s} are belong to us.\n", .{"codebase"});

    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    const alloc = gpa.allocator();

    const data = try readData(alloc);
    defer data.deinit();

    const total = try part1(data);
    std.debug.print("total: {d}\n", .{total});

    const score = try part2(data);
    std.debug.print("score: {d}\n", .{score});
}

fn getTestData(alloc: std.mem.Allocator) !Data {
    var lefts = std.ArrayList(i32).init(alloc);
    errdefer lefts.deinit();

    var rights = std.ArrayList(i32).init(alloc);
    errdefer rights.deinit();

    try lefts.append(3);
    try lefts.append(4);
    try lefts.append(2);
    try lefts.append(1);
    try lefts.append(3);
    try lefts.append(3);

    try rights.append(4);
    try rights.append(3);
    try rights.append(5);
    try rights.append(3);
    try rights.append(9);
    try rights.append(3);

    const data: Data = .{
        .lefts = lefts,
        .rights = rights,
    };
    sortData(data);

    return data;
}

test "part 1 example" {
    const data: Data = try getTestData(std.testing.allocator);
    defer data.deinit();
    const total = part1(data);
    try std.testing.expectEqual(total, 11);
}

test "part 2 example" {
    const data: Data = try getTestData(std.testing.allocator);
    defer data.deinit();
    const score = part2(data);
    try std.testing.expectEqual(score, 31);
}
