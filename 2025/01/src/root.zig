//! By convention, root.zig is the root source file when making a library.
const std = @import("std");

pub const State = struct {
    counter: usize = 0,
    current_val: i16 = 50,

    fn getDir(line: []const u8) i16 {
        return if (line[0] == 'R') 1 else -1;
    }

    fn getVal(line: []const u8) !i16 {
        const nbuf = line[1..];
        return try std.fmt.parseInt(i16, nbuf, 10);
    }

    fn getNext(self: State, line: []const u8) !i16 {
        const val = try getVal(line);
        const dir = getDir(line);
        return self.current_val + (val * dir);
    }

    pub fn init() State {
        return .{
            .counter = 0,
            .current_val = 50,
        };
    }

    pub fn part1(self: *State, line: []const u8) !void {
        const next = try self.getNext(line);
        self.current_val = @mod(next, 100);
        if (self.current_val == 0) {
            self.counter += 1;
        }
    }

    pub fn part2(self: *State, line: []const u8) !void {
        const dir: i16 = getDir(line);
        const next = try self.getNext(line);
        const last = self.current_val;
        const full_turns: usize = @intCast(@abs(@divFloor(next, 100)));

        if (last == 0 and dir == -1) {
            self.counter -= 1;
        }
        self.current_val = @mod(next, 100);
        self.counter += full_turns;
        if ((self.current_val == 0) and dir == -1) {
            self.counter += 1;
        }
    }

    pub fn printResult(self: State) void {
        std.debug.print("result: {d}\n", .{self.counter});
    }
};

test "left left" {
    var state = State.init();

    try state.part2("L50");
    try state.part2("L50");
    try std.testing.expectEqual(50, state.current_val);
    try std.testing.expectEqual(1, state.counter);
}

test "right right" {
    var state = State.init();

    try state.part2("R50");
    try state.part2("R50");
    try std.testing.expectEqual(50, state.current_val);
    try std.testing.expectEqual(1, state.counter);
}

test "right left" {
    var state = State.init();

    try state.part2("R50");
    try state.part2("L50");
    try std.testing.expectEqual(50, state.current_val);
    try std.testing.expectEqual(1, state.counter);
}

test "left right" {
    var state = State.init();

    try state.part2("L50");
    try state.part2("R50");
    try std.testing.expectEqual(50, state.current_val);
    try std.testing.expectEqual(1, state.counter);
}
