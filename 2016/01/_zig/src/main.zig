const std = @import("std");

const MoveData = struct {
    rot: u8,
    n: i16,
};

fn readInput(allocator: std.mem.Allocator) ![]MoveData {
    var f = try std.fs.cwd().openFile("data.txt", .{});
    defer f.close();
    var reader = std.io.bufferedReader(f.reader());
    var stream = reader.reader();
    var buf: [4096]u8 = undefined;
    var arr = std.ArrayList(MoveData).init(allocator);
    defer arr.deinit();

    while (try stream.readUntilDelimiterOrEof(&buf, '\n')) |line| {
        var ln = line;
        if (line[line.len - 1] == '\r') {
            ln = line[0..(line.len - 1)];
        }
        var iter = std.mem.split(u8, ln, ", ");
        while (iter.next()) |ins| {
            try arr.append(MoveData{
                .rot = ins[0],
                .n = try std.fmt.parseUnsigned(u8, ins[1..], 10),
            });
        }
    }
    return arr.toOwnedSlice();
}
const Point = struct {
    x: i16,
    y: i16,
};
fn getEndpoint(part: u8) !Point {
    const allocator = std.heap.page_allocator;
    const instructions: []MoveData = try readInput(allocator);
    defer allocator.free(instructions);
    var x: i16 = 0;
    var y: i16 = 0;
    var d: i8 = 0; // 0 = N, 1 = E, 2 = S, 3 = W
    var h = std.AutoHashMap(Point, void).init(allocator);
    try h.put(Point{ .x = x, .y = y }, {});

    for (instructions) |ins| {
        if (ins.rot == 'R') {
            d = @mod(d + 1, 4);
        } else {
            d = @mod(d - 1, 4);
        }
        const dx: i16 = switch (d) {
            0, 2 => 0,
            1 => 1,
            3 => -1,
            else => 0,
        };
        const dy: i16 = switch (d) {
            1, 3 => 0,
            0 => 1,
            2 => -1,
            else => 0,
        };

        if (part == 1) {
            x += dx * ins.n;
            y += dy * ins.n;
        } else {
            var i = ins.n;
            while (i > 0) : (i -= 1) {
                x += dx;
                y += dy;
                const p = Point{ .x = x, .y = y };
                const v = try h.getOrPut(p);
                if (v.found_existing) {
                    return p;
                } else {
                    v.value_ptr.* = {};
                }
            }
        }
    }
    return Point{ .x = x, .y = y };
}

fn startTimer() i64 {
    return std.time.milliTimestamp();
}

fn stopTimer(started: i64, p: Point) !void {
    const end = std.time.milliTimestamp();
    const dist = try std.math.absInt(p.x) + try std.math.absInt(p.y);
    std.debug.print("end: {d},{d} dist: {d}\n", .{ p.x, p.y, dist });
    std.debug.print("in {d} ms\n\n", .{end - started});
}

pub fn main() !void {
    var start = startTimer();
    var p = try getEndpoint(1);
    try stopTimer(start, p);

    start = startTimer();
    p = try getEndpoint(2);
    try stopTimer(start, p);
}
