const std = @import("std");

const timestamp = std.time.milliTimestamp;
const print = std.debug.print;

const Timer = @This();

ts_start: i64,
ts_end: i64,

pub fn start() Timer {
    return .{
        .ts_start = timestamp(),
        .ts_end = 0,
    };
}

pub fn end(self: *Timer) void {
    self.ts_end = timestamp();
}

pub fn printStats(self: Timer) void {
    const runtime = self.ts_end - self.ts_start;
    print("\n\nellapsed time:", .{});
    if (runtime > 60000) {
        print(" {d}m,", .{@divTrunc(runtime, 60000)});
    }
    if (runtime > 1000) {
        print(" {d}s,", .{@divTrunc(runtime, 1000)});
    }
    print(" {d}ms\n", .{@mod(runtime, 1000)});
}
