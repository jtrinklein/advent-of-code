const std = @import("std");

pub const Part = enum { one, two };

fn log(comptime fmt: []const u8, args: anytype) void {
    std.debug.print(fmt ++ "\n", args);
}

pub const State = struct {
    count: u128,
    last: u256,
    part: Part,
    alloc: std.mem.Allocator,
    first: bool,
    paths: [256]u64 = .{0} ** 256,

    pub fn init(alloc: std.mem.Allocator, part: Part) State {
        // const paths = alloc.alloc(u16, 256) catch {
        //     return []
        // }
        // std.mem.zeroes(paths);
        return .{
            .first = true,
            .count = 0,
            .last = 0,
            .part = part,
            .alloc = alloc,
        };
    }

    pub fn deinit(self: *State) void {
        _ = self;
    }

    fn lineToVal(line: []const u8) u256 {
        var val: u256 = 0;
        for (line) |c| {
            val <<= 1;
            if (c != '.') {
                val += 1;
            }
        }
        return val;
    }

    fn bitCount(v: u256) u16 {
        var count: u16 = 0;
        var val = v;
        while (val > 0) {
            defer val >>= 1;
            count += if (val & 1 == 1) 1 else 0;
        }
        return count;
    }

    pub fn processLine(self: *State, line: []const u8) !void {
        if (self.part == .one) {
            try self.part1Line(line);
        } else {
            try self.part2Line(line);
        }
    }

    fn part1Line(self: *State, line: []const u8) !void {
        const v = lineToVal(line);
        if (self.first) {
            self.last = v;
            self.first = false;
            return;
        }
        // log("--------------------------- {s}", .{line});

        const l = v << 1;
        const r = v >> 1;
        const no_split = (self.last & ~v);
        const splits = self.last & v;
        self.count += bitCount(splits);

        self.last = l | r | no_split;
        // log("--------------------------- {b:0>15}", .{self.last});
        // log("{b:0>15}", .{self.last});
    }

    fn updatePathsFromValue(self: *State, value: u256) void {
        var ii: usize = 0;
        var v = value;
        while (v > 0) {
            defer ii += 1;
            defer v >>= 1;
            if (v & 1 == 1) {
                self.paths[ii] += 1;
            }
        }
    }

    fn part2Line(self: *State, line: []const u8) !void {
        const v = lineToVal(line);
        if (self.first) {
            self.updatePathsFromValue(v);
            self.last = v;
            self.first = false;
            return;
        }

        const l = v << 1;
        const r = v >> 1;
        const no_split = (self.last & ~v);

        var splits = self.last & v;
        var i: usize = 0;
        while (splits > 0) {
            defer i += 1;
            defer splits >>= 1;
            if (splits & 1 == 1) {
                // this is eliminated transfer values left and right
                const e_val = self.paths[i];
                self.paths[i] = 0;

                if (i + 1 < 256) {
                    self.paths[i + 1] += e_val;
                }

                if (i > 0) {
                    self.paths[i - 1] += e_val;
                }
            }
        }

        self.last = l | r | no_split;
    }

    pub fn computeResult(self: *State) void {
        if (self.part == .one) {
            return;
        }

        self.count = 0;
        for (0..self.paths.len) |i| {
            self.count += self.paths[i];
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

    try std.testing.expectEqual(21, state.count);

    state.deinit();
}

test "part 2 example" {
    var state = State.init(std.testing.allocator, .two);
    var it = getTestLines();
    while (it.next()) |line| {
        try state.processLine(line);
    }

    state.computeResult();

    try std.testing.expectEqual(40, state.count);

    state.deinit();
}

test "line2val" {
    var v = State.lineToVal(".......s");
    try std.testing.expectEqual(1, v);

    v = State.lineToVal("s");
    try std.testing.expectEqual(1, v);

    v = State.lineToVal("s....");
    try std.testing.expectEqual(16, v);

    v = State.lineToVal("....s....");
    try std.testing.expectEqual(16, v);

    v = State.lineToVal("....s...s");
    try std.testing.expectEqual(17, v);

    v = State.lineToVal("....^^^^....^^^^....");
    try std.testing.expectEqual(0xF0F0, v);
}

test "bitCount 0xF0" {
    const v = State.bitCount(0xF0);
    try std.testing.expectEqual(4, v);
}
test "bitCount 0xFF" {
    const v = State.bitCount(0xFF);
    try std.testing.expectEqual(8, v);
}

test "bitCount 0xCC" {
    const v = State.bitCount(0xCC);
    try std.testing.expectEqual(4, v);
}

test "bitCount 0x33" {
    const v = State.bitCount(0x33);
    try std.testing.expectEqual(4, v);
}

test "bitCount 0x3C" {
    const v = State.bitCount(0x3C);
    try std.testing.expectEqual(4, v);
}
