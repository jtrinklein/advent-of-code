const std = @import("std");

const timestamp = std.time.milliTimestamp;

const Timer = @This();

running: bool,
ts_start: i64,
ts_end: i64,

pub fn start() Timer {
    return .{
        .running = true,
        .ts_start = timestamp(),
        .ts_end = 0,
    };
}

pub fn restart(self: *Timer) void {
    self.running = true;
    self.ts_start = timestamp();
    self.ts_end = 0;
}

pub fn getTime(self: Timer) i64 {
    if (self.running)
        return timestamp() - self.ts_start;

    return self.ts_end - self.ts_start;
}

pub fn end(self: *Timer) void {
    self.running = false;
    self.ts_end = timestamp();
}

// output ellapsed time
pub fn printStats(self: Timer, comptime printFn: fn (comptime fmt: []const u8, args: anytype) void) void {
    const runtime = self.getTime();

    printFn("\n\nellapsed time:", .{});
    if (runtime > 60000) {
        printFn(" {d}m,", .{@divTrunc(runtime, 60000)});
    }
    if (runtime > 1000) {
        printFn(" {d}s,", .{@divTrunc(runtime, 1000)});
    }
    printFn(" {d}ms\n", .{@mod(runtime, 1000)});
}
