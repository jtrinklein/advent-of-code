const std = @import("std");
const Data = @import("data.zig");

pub fn readData(alloc: std.mem.Allocator, filename: []const u8, data: *Data, comptime line_action: fn (d: *Data, line: []const u8) anyerror!void) !void {
    var file = try std.fs.cwd().openFile(filename, .{});
    defer file.close();

    // var buf_read = std.io.bufferedReader(file.reader());
    // var in_stream = buf_read.reader();
    const line = try file.reader().readAllAlloc(alloc, 65535);
    defer alloc.free(line);
    const trimmed = if (@import("builtin").os.tag == .windows)
        std.mem.trimRight(u8, line, "\r")
    else
        line;
    try line_action(data, trimmed);
}
