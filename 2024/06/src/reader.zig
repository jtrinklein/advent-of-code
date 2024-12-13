const std = @import("std");
const Data = @import("data.zig");

pub fn readData(filename: []const u8, data: *Data, comptime line_action: fn (d: *Data, line: []const u8) anyerror!void) !void {
    var file = try std.fs.cwd().openFile(filename, .{});
    defer file.close();

    var buf_read = std.io.bufferedReader(file.reader());
    var in_stream = buf_read.reader();
    var buf: [4096]u8 = undefined;

    while (try in_stream.readUntilDelimiterOrEof(&buf, '\n')) |line| {
        const trimmed = if (@import("builtin").os.tag == .windows)
            std.mem.trimRight(u8, line, "\r")
        else
            line;
        try line_action(data, trimmed);
    }
}
