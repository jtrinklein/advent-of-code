const std = @import("std");

const Report = struct {
    deltas: std.ArrayList(i8),
    levels: std.ArrayList(i8),

    const ReportStats = struct {
        num_big_step: u8,
        num_less: u8,
        num_more: u8,
        num_dupes: u8, //consecutive duplicate values

        pub fn noFlips(self: ReportStats) bool {
            return self.num_less == 0 or self.num_more == 0;
        }

        pub fn oneFlip(self: ReportStats) bool {
            return self.num_less == 1 or self.num_more == 1;
        }
    };

    fn getDeltaStats(deltas: std.ArrayList(i8)) ReportStats {
        var num_less: u8 = 0;
        var num_more: u8 = 0;
        var num_big_step: u8 = 0;
        var num_dupes: u8 = 0;
        for (deltas.items) |d| {
            if (d > 0) {
                num_more += 1;
            } else if (d < 0) {
                num_less += 1;
            } else {
                num_dupes += 1;
            }
            if (@abs(d) > 3) {
                num_big_step += 1;
            }
        }
        return .{
            .num_big_step = num_big_step,
            .num_less = num_less,
            .num_more = num_more,
            .num_dupes = num_dupes,
        };
    }
    fn getStats(self: Report) ReportStats {
        return Report.getDeltaStats(self.deltas);
    }

    fn areDeltasSafe(deltas: std.ArrayList(i8)) bool {
        const stats = Report.getDeltaStats(deltas);
        return stats.num_dupes == 0 and stats.noFlips() and stats.num_big_step == 0;
    }

    pub fn isSafe(self: Report) bool {
        return Report.areDeltasSafe(self.deltas);
    }

    pub fn isSafeWithDampener(self: Report) !bool {
        if (self.isSafe()) {
            return true;
        }
        const stats = self.getStats();
        if (stats.num_dupes > 1) {
            // 2 or more dupes is not fixable
            return false;
        }
        if (!(stats.oneFlip() or stats.noFlips())) {
            // 2 ore more flips is not fixable
            return false;
        }

        if (stats.noFlips()) {
            if (stats.num_dupes > 0 and stats.num_big_step > 0) {
                //cant fix big step and dupe
                return false;
            }
            if (stats.num_dupes == 1) {
                // a single dupe can be fixed
                return true;
            }
            if (stats.num_big_step == 1 and (@abs(self.deltas.items[0]) > 3 or @abs(self.deltas.items[self.deltas.items.len - 1]) > 3)) {
                // one big step at start or end is fixable
                return true;
            }

            return false;
        }

        // fixing a single flip=====

        // flip with dupe is unsolvable
        if (stats.num_dupes == 1) {
            return false;
        }

        // one flip can be fixed if its the last or the sum of that delta and the next is <= 3

        for (self.deltas.items, 0..) |d, i| {
            const is_flip = (stats.num_less == 1 and d < 0) or (stats.num_more == 1 and d > 0);
            if (!is_flip) {
                continue;
            }

            const is_last = i == self.deltas.items.len - 1;
            const is_first = i == 0;
            var new_deltas = try self.deltas.clone();
            defer new_deltas.deinit();
            const flip_delta = new_deltas.orderedRemove(i);

            // try removing second element of delta pair
            if (!is_last) {
                new_deltas.items[i] += flip_delta;
            }
            if (Report.areDeltasSafe(new_deltas)) {
                return true;
            }

            // undo attempt
            if (!is_last) {
                new_deltas.items[i] -= flip_delta;
            }

            // try removing first element of delta pair
            if (!is_first) {
                new_deltas.items[i - 1] += flip_delta;
            }
            if (Report.areDeltasSafe(new_deltas)) {
                return true;
            }

            return false;
        }

        unreachable;
    }

    pub fn init(alloc: std.mem.Allocator, data: []const u8) !Report {
        var levels = std.ArrayList(i8).init(alloc);
        errdefer levels.deinit();

        var deltas = std.ArrayList(i8).init(alloc);
        errdefer deltas.deinit();

        var it = std.mem.splitSequence(u8, data, " ");
        var is_first = true;
        var last: i8 = undefined;
        while (it.next()) |v| {
            const level = try std.fmt.parseInt(i8, v, 10);
            if (!is_first) {
                const delta = level - last;
                try deltas.append(delta);
            }
            last = level;
            is_first = false;
            try levels.append(level);
        }
        return .{
            .deltas = deltas,
            .levels = levels,
        };
    }
    pub fn deinit(self: Report) void {
        self.levels.deinit();
        self.deltas.deinit();
    }
};

const Data = struct {
    reports: std.ArrayList(Report),
    pub fn init(reports: std.ArrayList(Report)) Data {
        return .{
            .reports = reports,
        };
    }
    pub fn deinit(self: Data) void {
        for (self.reports.items) |r| {
            r.deinit();
        }
        self.reports.deinit();
    }
};

fn readData(alloc: std.mem.Allocator) !Data {
    var file = try std.fs.cwd().openFile("data.txt", .{});
    defer file.close();

    var buf_read = std.io.bufferedReader(file.reader());
    var in_stream = buf_read.reader();
    var buf: [1024]u8 = undefined;

    var reports = std.ArrayList(Report).init(alloc);
    errdefer reports.deinit();

    while (try in_stream.readUntilDelimiterOrEof(&buf, '\n')) |line| {
        const trimmed = if (@import("builtin").os.tag == .windows)
            std.mem.trimRight(u8, line, "\r")
        else
            line;
        try reports.append(try Report.init(alloc, trimmed));
    }

    return Data.init(reports);
}

pub fn main() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();

    const alloc = gpa.allocator();
    const data = try readData(alloc);
    defer data.deinit();

    const p1 = part1(data);
    std.debug.print("Reports with safe levels: {d}\n", .{p1});
    const p2 = try part2(data);
    std.debug.print("Reports with safe dampened levels: {d}\n", .{p2});
}

fn part1(data: Data) u32 {
    var safe_reports: u32 = 0;
    for (data.reports.items) |r| {
        if (r.isSafe()) {
            safe_reports += 1;
        }
    }
    return safe_reports;
}

fn part2(data: Data) !u32 {
    var safe_reports: u32 = 0;

    for (data.reports.items) |r| {
        if (try r.isSafeWithDampener()) {
            safe_reports += 1;
        }
    }
    return safe_reports;
}

fn getExampleData(alloc: std.mem.Allocator) !Data {
    var reports = std.ArrayList(Report).init(alloc);
    errdefer reports.deinit();
    try reports.append(try Report.init(alloc, "7 6 4 2 1"));
    try reports.append(try Report.init(alloc, "1 2 7 8 9"));
    try reports.append(try Report.init(alloc, "9 7 6 2 1"));
    try reports.append(try Report.init(alloc, "1 3 2 4 5"));
    try reports.append(try Report.init(alloc, "8 6 4 4 1"));
    try reports.append(try Report.init(alloc, "1 3 6 7 9"));
    return Data.init(reports);
}

test "example part 1" {
    const data = try getExampleData(std.testing.allocator);
    defer data.deinit();
    const value = part1(data);
    try std.testing.expectEqual(2, value);
}

test "report unsafe for last 2 levels" {
    const report = try Report.init(std.testing.allocator, "1 2 3 4 99");
    defer report.deinit();

    try std.testing.expectEqual(false, report.isSafe());
}

test "example part 2" {
    const data = try getExampleData(std.testing.allocator);
    defer data.deinit();
    const value = try part2(data);
    try std.testing.expectEqual(4, value);
}

test "report unsafe with dampener for dupe then flip with big step" {
    const report = try Report.init(std.testing.allocator, "11 11 13 12 11 10 8 4");
    defer report.deinit();

    try std.testing.expectEqual(false, try report.isSafeWithDampener());
}
test "report safe with last big step" {
    var report = try Report.init(std.testing.allocator, "1 2 3 4 5 99");
    defer report.deinit();

    try std.testing.expectEqual(true, try report.isSafeWithDampener());
}
test "report edge ascending flip and dupe as safe for part 2" {
    const report = try Report.init(std.testing.allocator, "7 10 8 10 11");
    defer report.deinit();

    try std.testing.expect(try report.isSafeWithDampener());
}
test "report edge descending flip and dupe as safe for part 2" {
    const report = try Report.init(std.testing.allocator, "29 28 27 25 26 25 22 20");
    defer report.deinit();
    try std.testing.expect(try report.isSafeWithDampener());
}
