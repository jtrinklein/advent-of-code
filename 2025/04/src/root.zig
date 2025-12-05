const std = @import("std");

fn log(comptime fmt: []const u8, args: anytype) void {
    std.debug.print(fmt ++ "\n", args);
}

pub const State = struct {
    // add any variables that need to be tracked here.
    data: std.ArrayList([]u8),
    alloc: std.mem.Allocator,
    part: u8,
    count: u32,

    const neighbor_limit: u8 = 3;

    pub fn init(alloc: std.mem.Allocator) State {
        return .{
            .count = 0,
            .part = 1,
            .data = .empty,
            .alloc = alloc,
        };
    }

    pub fn deinit(self: *State) void {
        // _ = self;
        for (self.data.items) |line| {
            self.alloc.free(line);
        }
        self.data.deinit(self.alloc);
    }

    fn getNeighbors(self: State, origin_x: usize, origin_y: usize) u8 {
        var count: u8 = 0;
        const max_x = self.data.items[origin_y].len - 1;
        const max_y = self.data.items.len - 1;
        const dy0: usize = if (origin_y == 0) 1 else 0;
        const dy1: usize = if (origin_y == max_y) 2 else 3;
        const dx0: usize = if (origin_x == 0) 1 else 0;
        const dx1: usize = if (origin_x == max_x) 2 else 3;
        for (dy0..dy1) |dy| {
            for (dx0..dx1) |dx| {
                if (dx == 1 and dy == 1) {
                    continue;
                }
                const x = origin_x + dx - 1;
                const y = origin_y + dy - 1;
                if (self.data.items[y][x] != '.') {
                    count += 1;
                }
            }
        }
        return count;
    }

    fn processPart1(self: *State) void {
        for (0..self.data.items.len) |y| {
            for (0..self.data.items[y].len) |x| {
                if (self.data.items[y][x] != '@') {
                    continue;
                }
                const neighbors = self.getNeighbors(x, y);
                if (neighbors <= neighbor_limit) {
                    self.count += 1;
                }
            }
        }
    }

    fn processPart2(self: *State) void {
        var accessible_rolls: u32 = 1;
        var x_to_fix: [4096]usize = undefined;
        var y_to_fix: [4096]usize = undefined;
        while (accessible_rolls > 0) {
            accessible_rolls = 0;
            for (0..self.data.items.len) |y| {
                for (0..self.data.items[y].len) |x| {
                    if (self.data.items[y][x] != '@') {
                        continue;
                    }
                    const neighbors = self.getNeighbors(x, y);
                    if (neighbors <= neighbor_limit) {
                        y_to_fix[accessible_rolls] = y;
                        x_to_fix[accessible_rolls] = x;
                        accessible_rolls += 1;
                    }
                }
            }
            self.count += accessible_rolls;
            for (0..accessible_rolls) |i| {
                const x = x_to_fix[i];
                const y = y_to_fix[i];
                self.data.items[y][x] = '.';
            }
        }
    }

    fn storeLine(self: *State, line: []const u8) !void {
        const dupe_line = try self.alloc.dupe(u8, line);
        try self.data.append(self.alloc, dupe_line);
    }

    pub fn part1(self: *State, line: []const u8) !void {
        try self.storeLine(line);
    }

    pub fn part2(self: *State, line: []const u8) !void {
        self.part = 2;
        try self.storeLine(line);
    }

    pub fn inputComplete(self: *State) void {
        // if processing needs to happen after the entire input is received, do it here
        if (self.part == 1) {
            self.processPart1();
        } else {
            self.processPart2();
        }
    }

    pub fn printResult(self: *State) void {
        std.debug.print("result: {d}\n", .{self.count});
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

// This is an example of how to write a useful test using the test inputs, you may also want to write tests for other parts of your program too
test "part 1 example" {
    const alloc = std.testing.allocator;
    var state = State.init(alloc);
    defer state.deinit();

    var it = getTestLines();
    while (it.next()) |line| {
        try state.part1(line);
    }

    state.inputComplete();

    // update the expectation depending on your solution.
    try std.testing.expectEqual(13, state.count);
}

test "part 2 example" {
    const alloc = std.testing.allocator;
    var state = State.init(alloc);
    defer state.deinit();

    var it = getTestLines();
    while (it.next()) |line| {
        try state.part2(line);
    }

    state.inputComplete();

    // update the expectation depending on your solution.
    try std.testing.expectEqual(43, state.count);
}

//TODO: add more tests
