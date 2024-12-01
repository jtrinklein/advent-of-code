const std = @import("std");

fn getData(alloc: std.mem.Allocator) !std.ArrayList([3]u16) {
    const file = try std.fs.cwd().openFile("data.txt", .{}); 
    defer file.close();

    var reader = std.io.bufferedReader(file.reader());
    var stream = reader.reader();
    var buf: [1024]u8 = undefined;
    var arr = std.ArrayList<[3]u16>.init(alloc);
    defer arr.deinit();
    
    while (try stream.readUntilDelimiterOrEof(&buf, '\n')) {}

    return arr;
}


pub fn main() !void {
    // Prints to stderr (it's a shortcut based on `std.io.getStdErr()`)
    std.debug.print("All your {s} are belong to us.\n", .{"codebase"});

    // stdout is for the actual output of your application, for example if you
    // are implementing gzip, then only the compressed bytes should be sent to
    // stdout, not any debugging messages.
    const stdout_file = std.io.getStdOut().writer();
    var bw = std.io.bufferedWriter(stdout_file);
    const stdout = bw.writer();

    try stdout.print("Run `zig build test` to run the tests.\n", .{});

    try bw.flush(); // don't forget to flush!
}

test "simple test" {
    var list = std.ArrayList(i32).init(std.testing.allocator);
    defer list.deinit(); // try commenting this out and see if zig detects the memory leak!
    try list.append(42);
    try std.testing.expectEqual(@as(i32, 42), list.pop());
}
