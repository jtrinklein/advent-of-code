const std = @import("std");

pub const Part = enum { one, two };

fn log(comptime fmt: []const u8, args: anytype) void {
    std.debug.print(fmt ++ "\n", args);
}

const Point = struct {
    x: u32,
    y: u32,
    z: u32,

    pub fn init(str: []const u8) !Point {
        const s1 = std.mem.indexOf(u8, str, .{','}) orelse return error.NoSeparator;
        const s2 = std.mem.indexOf(u8, str[s1 + 1 ..], .{','}) orelse return error.NoSeparator;
        const x = try std.fmt.parseInt(u32, str[0..s1], 10);
        const y = try std.fmt.parseInt(u32, str[s1 + 1 .. s2], 10);
        const z = try std.fmt.parseInt(u32, str[s2 + 1 ..], 10);
        return .{
            .x = x,
            .y = y,
            .z = z,
        };
    }

    pub fn dist(self: Point, p: Point) f64 {
        const dx = @as(i64, @intCast(self.x)) - @as(i64, @intCast(p.x));
        const dy = @as(i64, @intCast(self.y)) - @as(i64, @intCast(p.y));
        const dz = @as(i64, @intCast(self.z)) - @as(i64, @intCast(p.z));
        return @sqrt(@as(f64, @floatFromInt(dx * dx)) + @as(f64, @floatFromInt(dy * dy)) + @as(f64, @floatFromInt(dz * dz)));
    }
};

pub const State = struct {
    count: u16,
    part: Part,
    alloc: std.mem.Allocator,
    points: [1024]Point,
    n_points: u16,

    pub fn init(alloc: std.mem.Allocator, part: Part) State {
        return .{
            .count = 0,
            .part = part,
            .alloc = alloc,
            .points = .{0} ** 1024,
            .n_points = 0,
        };
    }

    pub fn deinit(self: *State) void {
        _ = self;
    }

    pub fn processLine(self: *State, line: []const u8) !void {
        self.points[self.n_points] = try Point.init(line);
        self.n_points += 1;
    }

    fn computePart1(self: *State) void {
        self.count = 0;
    }

    pub fn computeResult(self: *State) void {
        if (self.part == .one) {
            self.computePart1();
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

    try std.testing.expectEqual(0, state.count);

    state.deinit();
}
