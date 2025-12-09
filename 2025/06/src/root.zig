const std = @import("std");

pub const Part = enum { one, two };

fn log(comptime fmt: []const u8, args: anytype) void {
    std.debug.print(fmt ++ "\n", args);
}

pub const State = struct {
    num_idx: u8,
    nums: [4][1000]u64,
    num_lines: u8,
    ops: [1000]u8,
    result: u128,
    part: Part,
    alloc: std.mem.Allocator,
    problems: usize,
    lines: std.ArrayList([]u8),

    pub fn init(alloc: std.mem.Allocator, part: Part) State {
        return .{
            .problems = 1000,
            .num_lines = 0,
            .num_idx = 0,
            .nums = undefined,
            .ops = undefined,
            .result = 0,
            .part = part,
            .alloc = alloc,
            .lines = .empty,
        };
    }

    pub fn deinit(self: *State) void {
        for (self.lines.items) |x| {
            self.alloc.free(x);
        }
        self.lines.deinit(self.alloc);
    }

    pub fn processLine(self: *State, line: []const u8) !void {
        try self.lines.append(self.alloc, try self.alloc.dupe(u8, line));
        // if (self.part == .one) {
        //     try self.part1Line(line);
        // } else {
        //     try self.part2Line(line);
        // }
    }

    fn parseNumbersToLine(self: *State, nums_index: u8, line: []const u8) !void {
        var it = std.mem.splitScalar(u8, line, ',');
        var i: usize = 0;
        while (it.next()) |val| {
            self.nums[nums_index][i] = try std.fmt.parseInt(u64, val, 10);
            i += 1;
        }
    }

    fn parseOps(self: *State, line: []const u8) !void {
        var it = std.mem.splitScalar(u8, line, ',');
        var i: usize = 0;
        while (it.next()) |val| {
            self.ops[i] = val[0];
            i += 1;
        }
    }

    fn parseInputLine(self: *State, line: []const u8) !void {
        if (line.len == 0) {
            return error.EmptyLine;
        }

        if (line[0] >= '0' and line[0] <= '9') {
            try self.parseNumbersToLine(self.num_idx, line);
            self.num_idx += 1;
            self.num_lines += 1;
            return;
        }

        try self.parseOps(line);
    }

    fn part1Line(self: *State, line: []const u8) !void {
        try self.parseInputLine(line);
    }

    fn part2Line(self: *State, line: []const u8) !void {
        _ = self;
        _ = line;
    }

    pub fn computeResult(self: *State) void {
        if (self.part == .one) {
            self.solvePart1();
        } else {
            self.solvePart2();
        }
    }
    fn solvePart1(self: *State) void {
        self.result = 0;
        const num_lines = self.lines.items.len - 1;
        var iters: [4]NumIter = undefined;
        for (0..num_lines) |i| {
            iters[i] = NumIter.init(self.lines.items[i]);
        }
        var opIter = OpIter.init(self.lines.items[num_lines]);
        while (opIter.next()) |op| {
            var val: u64 = if (op == '*') 1 else 0;
            for (0..num_lines) |i| {
                const v = iters[i].next() orelse unreachable;
                val = if (op == '*') val * v else val + v;
            }
            self.result += val;
        }
    }
    fn solvePart2(self: *State) void {
        self.result = 0;
        const digits = self.lines.items.len - 1;
        var nums: [4]u64 = undefined;
        for (0..digits) |n| {
            nums[n] = 0;
        }

        const line_len = self.lines.items[0].len;
        var n_idx: usize = 0;
        for (0..line_len) |idx| {
            const i = line_len - idx - 1;
            const op = self.lines.items[digits][i];
            var num: u64 = 0;
            var skip = true;
            for (0..digits) |n| {
                const nv = self.lines.items[n][i];
                if (nv != ' ') {
                    skip = false;
                    num = num * 10 + (nv - '0');
                }
            }
            if (skip) {
                continue;
            }
            nums[n_idx] = num;
            n_idx += 1;

            if (op != ' ') {
                const is_mult = op == '*';
                var v: u128 = if (is_mult) 1 else 0;
                for (0..n_idx) |n| {
                    v = if (is_mult) v * nums[n] else v + nums[n];
                    nums[n] = 0;
                }
                n_idx = 0;
                self.result += v;
            }
        }
    }

    pub fn printResult(self: State) void {
        log("result: {d}", .{self.result});
    }
};

const OpIter = struct {
    line: []const u8,
    pos: usize,
    pub fn init(line: []const u8) OpIter {
        var pos: usize = 0;
        while (pos < line.len and line[pos] == ' ') {
            pos += 1;
        }

        return .{
            .pos = pos,
            .line = line,
        };
    }

    pub fn next(self: *OpIter) ?u8 {
        if (self.pos >= self.line.len) {
            return null;
        }

        const op = self.line[self.pos];
        self.pos += 1;
        while (self.pos < self.line.len and self.line[self.pos] == ' ') {
            self.pos += 1;
        }
        return op;
    }
};
const NumIter = struct {
    line: []const u8,
    pos: usize,
    pub fn init(line: []const u8) NumIter {
        var pos: usize = 0;
        while (pos < line.len and line[pos] == ' ') {
            pos += 1;
        }

        return .{
            .pos = pos,
            .line = line,
        };
    }

    pub fn next(self: *NumIter) ?u64 {
        if (self.pos >= self.line.len) {
            return null;
        }

        var val: u64 = 0;
        while (self.pos < self.line.len and self.line[self.pos] != ' ') {
            val = val * 10 + @as(u64, @intCast(self.line[self.pos] - '0'));
            self.pos += 1;
        }

        while (self.pos < self.line.len and self.line[self.pos] == ' ') {
            self.pos += 1;
        }

        return val;
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
    defer state.deinit();

    state.problems = 4; // only 4 in test set
    var it = getTestLines();
    while (it.next()) |line| {
        try state.processLine(line);
    }

    state.computeResult();

    try std.testing.expectEqual(4277556, state.result);
}

test "part 2 example" {
    var state = State.init(std.testing.allocator, .two);
    defer state.deinit();

    state.problems = 4; // only 4 in test set
    var it = getTestLines();
    while (it.next()) |line| {
        try state.processLine(line);
    }

    state.computeResult();

    try std.testing.expectEqual(3263827, state.result);
}

test "num iter" {
    var it = NumIter.init("123 34  4    5890 6 ");

    try std.testing.expectEqual(123, it.next() orelse unreachable);
    try std.testing.expectEqual(34, it.next() orelse unreachable);
    try std.testing.expectEqual(4, it.next() orelse unreachable);
    try std.testing.expectEqual(5890, it.next() orelse unreachable);
    try std.testing.expectEqual(6, it.next() orelse unreachable);
    try std.testing.expectEqual(null, it.next());

    it = NumIter.init(" 57 1");

    try std.testing.expectEqual(57, it.next() orelse unreachable);
    try std.testing.expectEqual(1, it.next() orelse unreachable);
    try std.testing.expectEqual(null, it.next());
}
test "op iter" {
    var it = OpIter.init("*   +   *  +   ");

    try std.testing.expectEqual('*', it.next() orelse unreachable);
    try std.testing.expectEqual('+', it.next() orelse unreachable);
    try std.testing.expectEqual('*', it.next() orelse unreachable);
    try std.testing.expectEqual('+', it.next() orelse unreachable);
    try std.testing.expectEqual(null, it.next());
}
