const std = @import("std");

pub const Part = enum { one, two };

fn log(comptime fmt: []const u8, args: anytype) void {
    std.debug.print(fmt ++ "\n", args);
}

pub const State = struct {
    ranges: [1024][2]u64,
    n_ranges: usize,
    ranges_done: bool,
    part: Part,
    count: u64,

    pub fn init(alloc: std.mem.Allocator, part: Part) State {
        _ = alloc;
        return .{
            .ranges = undefined,
            .n_ranges = 0,
            .ranges_done = false,
            .part = part,
            .count = 0,
        };
    }

    pub fn deinit(self: *State) void {
        _ = self;
    }

    pub fn processLine(self: *State, line: []const u8) !void {
        if (self.part == .one) {
            try self.part1Line(line);
        } else {
            try self.part2Line(line);
        }
    }
    fn sortRanges(self: *State) void {
        var swapped = true;
        while (swapped) {
            swapped = false;
            o: for (0..self.n_ranges) |i| {
                for (i..self.n_ranges) |j| {
                    if (self.ranges[j][0] < self.ranges[i][0]) {
                        const t = self.ranges[i];
                        self.ranges[i] = self.ranges[j];
                        self.ranges[j] = t;
                        swapped = true;
                        break :o;
                    }
                }
            }
        }
    }

    fn inRange(self: *State, v: u64) bool {
        for (0..self.n_ranges) |i| {
            if (self.ranges[i][0] <= v and v <= self.ranges[i][1]) {
                return true;
            }
        }
        return false;
    }

    fn addRange(self: *State, start: u64, end: u64) void {
        self.ranges[self.n_ranges] = .{ start, end };
        self.n_ranges += 1;
    }

    fn mergeRanges(self: *State) void {
        while (true) {
            var merged = self.n_ranges;
            main_loop: for (0..self.n_ranges) |i| {
                for (i + 1..self.n_ranges) |j| {
                    var ri = &self.ranges[i];
                    var rj = &self.ranges[j];

                    const ri0 = ri[0];
                    const ri1 = ri[1];
                    const rj0 = rj[0];
                    const rj1 = rj[1];

                    if (ri0 <= rj0 and rj0 <= ri1) {
                        ri[1] = @max(rj1, ri1);
                        merged = j;
                        break :main_loop;
                    }

                    if (ri0 <= rj1 and rj1 <= ri1) {
                        ri[0] = @min(rj0, ri0);
                        merged = j;
                        break :main_loop;
                    }

                    if (rj0 <= ri0 and ri0 <= rj1) {
                        rj[1] = @max(rj1, ri1);
                        merged = i;
                        break :main_loop;
                    }

                    if (rj0 <= ri1 and ri1 <= rj1) {
                        rj[0] = @min(rj1, ri1);
                        merged = i;
                        break :main_loop;
                    }

                    if (ri1 + 1 == rj0) {
                        // ri is before rj
                        ri[1] = rj1;
                        merged = j;
                        break :main_loop;
                    }

                    if (rj1 + 1 == ri0) {
                        // rj is before ri
                        ri[0] = rj0;
                        merged = j;
                        break :main_loop;
                    }
                }
            }

            if (merged == self.n_ranges) {
                break;
            }

            for (merged..self.n_ranges - 1) |i| {
                self.ranges[i] = self.ranges[i + 1];
            }

            self.n_ranges -= 1;
        }
    }
    fn rangeLess(_: void, lhs: [2]u64, rhs: [2]u64) bool {
        return lhs[0] < rhs[0];
    }

    fn printRanges(self: State) void {
        for (0..self.n_ranges) |i| {
            log("{d} - {d}", .{ self.ranges[i][0], self.ranges[i][1] });
        }
    }

    fn addRangeLine(self: *State, line: []const u8) !void {
        var it = std.mem.splitScalar(u8, line, '-');
        const s = it.next() orelse unreachable;
        const e = it.next() orelse unreachable;

        const start = try std.fmt.parseInt(u64, s, 10);
        const end = try std.fmt.parseInt(u64, e, 10);
        self.addRange(start, end);
    }

    fn part1Line(self: *State, line: []const u8) !void {
        if (line.len == 0 and !self.ranges_done) {
            self.ranges_done = true;
            self.mergeRanges();
            return;
        }

        if (!self.ranges_done) {
            try self.addRangeLine(line);
            return;
        }

        const v = try std.fmt.parseInt(u64, line, 10);
        if (self.inRange(v)) {
            self.count += 1;
        }
    }

    fn part2Line(self: *State, line: []const u8) !void {
        if (self.ranges_done) {
            return;
        }
        if (line.len == 0) {
            self.ranges_done = true;
            self.mergeRanges();
            return;
        }
        try self.addRangeLine(line);
    }

    pub fn computeResult(self: *State) void {
        if (self.part == .one) {
            return;
        }
        self.count = 0;
        for (0..self.n_ranges) |i| {
            const r = self.ranges[i];
            self.count += r[1] - r[0] + 1;
        }
    }

    pub fn printResult(self: State) void {
        log("result: {d}", .{self.count});
    }
};

const LineIterator = struct {
    lines: std.mem.SplitIterator(u8, .scalar) = undefined,

    pub fn init(data: []const u8) LineIterator {
        const lines = std.mem.splitScalar(u8, data, '\n');
        return .{
            .lines = lines,
        };
    }

    pub fn next(self: *LineIterator) ?[]const u8 {
        const maybe_line = self.lines.next();
        if (maybe_line) |line| {
            return if (line[line.len - 1] == '\r') line[0 .. line.len - 1] else line;
        }
        return null;
    }
};

fn getTestLines() LineIterator {
    const data = @embedFile("./test.txt");
    return LineIterator.init(data);
}

test "part 1 example" {
    var state = State.init(std.testing.allocator, .one);
    var it = getTestLines();
    while (it.next()) |line| {
        try state.processLine(line);
    }

    state.computeResult();

    try std.testing.expectEqual(3, state.count);
}

test "part 2 example" {
    var state = State.init(std.testing.allocator, .two);
    var it = getTestLines();
    while (it.next()) |line| {
        try state.processLine(line);
    }

    state.computeResult();

    try std.testing.expectEqual(14, state.count);
}

test "merge example ranges" {
    var state = State.init(std.testing.allocator, .one);
    state.ranges[0] = .{ 3, 5 };
    state.ranges[1] = .{ 10, 14 };
    state.ranges[2] = .{ 16, 20 };
    state.ranges[3] = .{ 12, 18 };
    state.n_ranges = 4;

    state.mergeRanges();

    try std.testing.expectEqual(2, state.n_ranges);
    try std.testing.expectEqual(3, state.ranges[0][0]);
    try std.testing.expectEqual(5, state.ranges[0][1]);
    try std.testing.expectEqual(10, state.ranges[1][0]);
    try std.testing.expectEqual(20, state.ranges[1][1]);
}

test "merge ranges" {
    var state = State.init(std.testing.allocator, .one);
    state.ranges[0] = .{ 1, 20 };
    state.ranges[1] = .{ 35, 55 };
    state.ranges[2] = .{ 15, 25 };
    state.ranges[3] = .{ 25, 59 };
    state.n_ranges = 4;

    state.mergeRanges();

    try std.testing.expectEqual(1, state.n_ranges);
    try std.testing.expectEqual(1, state.ranges[0][0]);
    try std.testing.expectEqual(59, state.ranges[0][1]);
}

test "merge ranges no merge" {
    var state = State.init(std.testing.allocator, .one);
    state.ranges[0] = .{ 1, 20 };
    state.ranges[1] = .{ 22, 55 };
    state.ranges[2] = .{ 115, 215 };
    state.ranges[3] = .{ 252, 592 };
    state.n_ranges = 4;

    state.mergeRanges();

    try std.testing.expectEqual(4, state.n_ranges);
}

test "merge ranges neighbors" {
    var state = State.init(std.testing.allocator, .one);
    state.ranges[0] = .{ 1, 20 };
    state.ranges[1] = .{ 57, 58 };
    state.ranges[2] = .{ 51, 55 };
    state.ranges[3] = .{ 21, 50 };
    state.n_ranges = 4;

    state.mergeRanges();

    try std.testing.expectEqual(2, state.n_ranges);
    try std.testing.expectEqual(1, state.ranges[0][0]);
    try std.testing.expectEqual(55, state.ranges[0][1]);
    try std.testing.expectEqual(57, state.ranges[1][0]);
    try std.testing.expectEqual(58, state.ranges[1][1]);
}
