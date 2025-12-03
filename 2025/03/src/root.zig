const std = @import("std");

fn log(comptime fmt: []const u8, args: anytype) void {
    std.debug.print(fmt ++ "\n", args);
}

const T = u64;
pub const State = struct {
    total: T,
    pub fn init() State {
        return .{
            .total = 0,
        };
    }

    fn digitVal(c: u8) T {
        return c - '0';
    }

    pub fn part1(self: *State, line: []const u8) !void {
        try self.getJoltage(line, 2);
    }
    fn getJoltage(self: *State, line: []const u8, batteries: usize) !void {
        // log("row: {s}", .{line});
        var row_value: T = 0;
        var i: usize = 0;
        var max: u8 = 0;
        var last_idx = line.len;
        var current_idx = line.len;
        var n_batteries = batteries;
        while (n_batteries > 0) {
            defer n_batteries -= 1;
            i = n_batteries - 1;
            row_value *= 10;
            max = 0;
            while (i < last_idx) {
                defer i += 1;
                const j = line.len - i - 1;
                const v = line[j];
                if (v >= max) {
                    max = v;
                    current_idx = i;
                }
            }
            row_value += digitVal(max);
            last_idx = current_idx;
        }
        // log("row value: {d}", .{row_value});
        self.total += row_value;
    }

    pub fn part2(self: *State, line: []const u8) !void {
        try self.getJoltage(line, 12);
    }

    pub fn printResult(self: State) void {
        std.debug.print("result: {d}\n", .{self.total});
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
    var state = State.init();
    var it = getTestLines();
    while (it.next()) |line| {
        try state.part1(line);
    }

    try std.testing.expectEqual(357, state.total);
}

test "part 2 example" {
    var state = State.init();
    var it = getTestLines();
    while (it.next()) |line| {
        try state.part2(line);
    }

    try std.testing.expectEqual(3121910778619, state.total);
}
