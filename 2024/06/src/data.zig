const std = @import("std");

const Data = @This();

const Direction = enum {
    up,
    down,
    left,
    right,
};

alloc: std.mem.Allocator,
map: std.ArrayList([]u8),
orig_map: std.ArrayList([]u8),
start_y: usize,
start_x: usize,

pub fn processInputLine(self: *Data, line: []const u8) !void {
    const x = try self.alloc.alloc(u8, line.len);
    errdefer self.alloc.free(x);
    const y = try self.alloc.alloc(u8, line.len);
    errdefer self.alloc.free(y);

    @memcpy(x, line);
    @memcpy(y, line);
    try self.map.append(x);
    try self.orig_map.append(y);
}
pub fn getPart1Value(self: *Data) !u32 {
    var x: usize = 0;
    var y: usize = 0;
    for (self.map.items, 0..) |line, yi| {
        for (line, 0..) |c, xi| {
            if (c == '^') {
                x = xi;
                y = yi;
                break;
            }
        }
        if (x != 0) {
            break;
        }
    }
    self.start_y = y;
    self.start_x = x;
    var visited: u32 = 1;
    var since_last_empty: u32 = 0;
    var d = Direction.up;
    var new_x: usize = 0;
    var new_y: usize = 0;
    const height = self.map.items.len;
    const width = self.map.items[0].len;

    while (true) {
        var next_d = d;
        switch (d) {
            .up => {
                if (y == 0) {
                    return visited;
                }
                new_y = y - 1;
                new_x = x;
                next_d = Direction.right;
            },
            .down => {
                if ((y + 1) == height) {
                    return visited;
                }
                new_y = y + 1;
                new_x = x;
                next_d = Direction.left;
            },
            .left => {
                if (x == 0) {
                    return visited;
                }
                new_x = x - 1;
                new_y = y;
                next_d = Direction.up;
            },
            .right => {
                if (x + 1 == width) {
                    return visited;
                }
                new_x = x + 1;
                new_y = y;
                next_d = Direction.down;
            },
        }
        const c = self.map.items[new_y][new_x];
        if (c == '.') {
            visited += 1;
            since_last_empty = 0;
            self.map.items[y][x] = 'X';
            x = new_x;
            y = new_y;
        } else if (c == '#') {
            d = next_d;
        } else {
            since_last_empty += 1;
            if (self.map.items[y][x] == '.') {
                self.map.items[y][x] = 'X';
            }
            x = new_x;
            y = new_y;
        }

        if (since_last_empty > (width * height)) {
            return error.InfiniteLoop;
        }
    }
    unreachable;
}

fn resetMap(self: Data) void {
    for (0..self.map.items.len) |i| {
        @memcpy(self.map.items[i], self.orig_map.items[i]);
    }
}

pub fn getPart2Value(self: *Data) u32 {
    var count: u32 = 0;
    var locations = std.ArrayList([2]usize).init(self.alloc);
    defer locations.deinit();

    for (self.map.items, 0..) |line, y| {
        for (line, 0..) |c, x| {
            if (y == self.start_y and x == self.start_x) {
                continue;
            }
            if (c == 'X' or c == '.') {
                locations.append(.{ x, y }) catch {
                    return 0;
                };
            }
        }
    }
    for (locations.items) |loc| {
        self.resetMap();
        self.map.items[loc[1]][loc[0]] = '#';

        const result = self.getPart1Value() catch 0;
        if (result == 0) {
            count += 1;
        }
    }
    return count;
}
fn printMap(self: Data) void {
    std.debug.print("\n\n", .{});

    for (self.map.items) |line| {
        std.debug.print("{s}\n", .{line});
    }
}

pub fn init(alloc: std.mem.Allocator) Data {
    const map = std.ArrayList([]u8).init(alloc);
    const orig_map = std.ArrayList([]u8).init(alloc);
    return .{
        .alloc = alloc,
        .map = map,
        .orig_map = orig_map,
        .start_y = 0,
        .start_x = 0,
    };
}

pub fn deinit(self: Data) void {
    for (0..self.map.items.len) |i| {
        self.alloc.free(self.map.items[i]);
        self.alloc.free(self.orig_map.items[i]);
    }
    self.map.deinit();
    self.orig_map.deinit();
}
