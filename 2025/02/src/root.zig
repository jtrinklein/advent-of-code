//! By convention, root.zig is the root source file when making a library.
const std = @import("std");

fn log(comptime fmt: []const u8, args: anytype) void {
    std.debug.print(fmt ++ "\n", args);
}
pub const State = struct {
    total: u64,
    pub fn init() State {
        return .{
            .total = 0,
        };
    }

    pub fn part1(self: *State, line: []const u8) !void {
        self.total = 0;
        var rangeIt = std.mem.splitScalar(u8, line, ',');
        while (rangeIt.next()) |range| {
            var valIt = std.mem.splitScalar(u8, range, '-');
            const startStr = valIt.next() orelse "0";
            const endStr = valIt.next() orelse "0";
            const start = try std.fmt.parseInt(u64, startStr, 10);
            const end = try std.fmt.parseInt(u64, endStr, 10);

            if (startStr.len % 2 == 1 and endStr.len == startStr.len) {
                continue;
            }

            var n = start;
            var buf: [4096]u8 = undefined;
            while (n <= end) {
                defer n += 1;

                const nstr = try std.fmt.bufPrint(&buf, "{d}", .{n});
                if (nstr.len % 2 == 1) {
                    if (endStr.len == nstr.len) {
                        break;
                    }
                    n = @min(std.math.pow(u64, 10, nstr.len), end) - 1;
                    continue;
                }

                const halfLen = nstr.len / 2;
                if (std.mem.eql(u8, nstr[0..halfLen], nstr[halfLen..])) {
                    // log("{s} has invalid id {s}", .{ range, nstr });
                    self.total += n;
                }
            }
        }
    }

    pub fn part2(self: *State, line: []const u8) !void {
        self.total = 0;
        var rangeIt = std.mem.splitScalar(u8, line, ',');
        while (rangeIt.next()) |range| {
            var valIt = std.mem.splitScalar(u8, range, '-');
            const startStr = valIt.next() orelse "0";
            const endStr = valIt.next() orelse "0";
            const start = try std.fmt.parseInt(u64, startStr, 10);
            const end = try std.fmt.parseInt(u64, endStr, 10);

            var n = start;
            var buf: [4096]u8 = undefined;
            id_loop: while (n <= end) {
                defer n += 1;

                const nstr = try std.fmt.bufPrint(&buf, "{d}", .{n});
                const halfLen = @divFloor(nstr.len, 2);
                var len: usize = 1;

                len_loop: while (len <= halfLen) {
                    defer len += 1;
                    if (@mod(nstr.len, len) != 0) {
                        continue;
                    }
                    const patternCount = @divFloor(nstr.len, len);
                    var i: usize = 0;
                    while (i < len) {
                        defer i += 1;
                        var j: usize = 1;
                        const digit = nstr[i];
                        while (j < patternCount) {
                            defer j += 1;
                            const idx = j * (len) + i;
                            const val = nstr[idx];
                            // log("pattern: {d} compare idx: {d}, to idx: {d}, {c} should match {c}", .{ j, idx, i, val, digit });
                            if (val != digit) {
                                continue :len_loop;
                            }
                        }
                    }
                    // log("{s} has invalid id {s}", .{ range, nstr });
                    self.total += n;
                    continue :id_loop;
                }
            }
        }
    }

    pub fn printResult(self: State) void {
        std.debug.print("result: {d}\n", .{self.total});
    }
};

test "part 1 example" {
    const test_data = @embedFile("./test.txt");
    var state = State.init();
    try state.part1(test_data);

    try std.testing.expectEqual(1227775554, state.total);
}

test "part 2 example" {
    const test_data = @embedFile("./test.txt");
    var state = State.init();
    try state.part2(test_data);
    try std.testing.expectEqual(4174379265, state.total);
}

test "three 3 len patterns" {
    var state = State.init();
    try state.part2("824824823-824824824");
    try std.testing.expectEqual(824824824, state.total);
}
