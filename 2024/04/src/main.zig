const std = @import("std");

const print = std.debug.print;
const Data = struct {
    grid: std.ArrayList(std.ArrayList(u8)),
    alloc: std.mem.Allocator,

    fn findWord(self: Data, word: []const u8) !u16 {
        var count: u16 = 0;
        var backWords = std.ArrayList(u8).init(self.alloc);
        defer backWords.deinit();
        for (0..word.len) |i| {
            try backWords.append(word[word.len - i - 1]);
        }
        print("find: {s} or {s}\n", .{ word, backWords.items[0..] });
        for (self.grid.items, 0..) |line, y| {
            for (0..line.items.len) |x| {
                if (x <= line.items.len - word.len) {
                    const window = line.items[x .. x + word.len];
                    // forward
                    if (std.mem.eql(u8, window, word)) {
                        count += 1;
                    }
                    // backward
                    if (std.mem.eql(u8, window, backWords.items)) {
                        count += 1;
                    }
                }

                var down_match = true;
                var up_match = true;
                var back_down_match = true;
                var back_up_match = true;
                var forward_down_match = true;
                var forward_up_match = true;
                for (0..word.len) |i| {
                    const yi = y + i;
                    const xi = x + i;
                    const xmi = @as(i32, @intCast(x)) - @as(i32, @intCast(i));
                    if (yi >= self.grid.items.len or x >= self.grid.items[yi].items.len) {
                        down_match = false;
                        up_match = false;
                    }
                    if (yi >= self.grid.items.len or xi >= self.grid.items[yi].items.len) {
                        back_down_match = false;
                        back_up_match = false;
                    }
                    if (yi >= self.grid.items.len or xmi < 0) {
                        forward_down_match = false;
                        forward_up_match = false;
                    }

                    if (!forward_down_match or self.grid.items[yi].items[@intCast(xmi)] != word[i]) {
                        forward_down_match = false;
                    }
                    if (!forward_up_match or self.grid.items[yi].items[@intCast(xmi)] != backWords.items[i]) {
                        forward_up_match = false;
                    }
                    if (!back_down_match or self.grid.items[yi].items[xi] != word[i]) {
                        back_down_match = false;
                    }
                    if (!back_up_match or self.grid.items[yi].items[xi] != backWords.items[i]) {
                        back_up_match = false;
                    }
                    if (!down_match or self.grid.items[yi].items[x] != word[i]) {
                        down_match = false;
                    }
                    if (!up_match or self.grid.items[yi].items[x] != backWords.items[i]) {
                        up_match = false;
                    }
                    if (!down_match and !up_match and !back_down_match and !back_up_match and !forward_down_match and !forward_up_match) {
                        break;
                    }
                }
                if (down_match) {
                    count += 1;
                }
                if (up_match) {
                    count += 1;
                }
                if (forward_down_match) {
                    count += 1;
                }
                if (forward_up_match) {
                    count += 1;
                }
                if (back_down_match) {
                    count += 1;
                }
                if (back_up_match) {
                    count += 1;
                }
            }
        }
        return count;
    }
    fn findCrossMas(self: Data) u16 {
        var count: u16 = 0;
        const mas = "MAS";
        const sam = "SAM";
        for (0..self.grid.items.len - 2) |y| {
            for (0..self.grid.items[y].items.len - 2) |x| {
                var f_sam: u8 = 1;
                var f_mas: u8 = 1;
                var b_sam: u8 = 1;
                var b_mas: u8 = 1;
                for (0..3) |i| {
                    // f = /
                    const f = self.grid.items[y + 2 - i].items[x + i];
                    // b = \
                    const b = self.grid.items[y + i].items[x + i];

                    // / sam
                    if (f_sam == 1 and f != sam[i]) {
                        f_sam = 0;
                    }
                    // \ sam
                    if (b_sam == 1 and b != sam[i]) {
                        b_sam = 0;
                    }
                    // / mas
                    if (f_mas == 1 and f != mas[i]) {
                        f_mas = 0;
                    }
                    // \ mas
                    if (b_mas == 1 and b != mas[i]) {
                        b_mas = 0;
                    }
                }
                if ((f_sam + f_mas + b_sam + b_mas) == 2) {
                    count += 1;
                }
            }
        }
        return count;
    }
    pub fn findXmas(self: Data) u16 {
        const count = self.findWord("XMAS") catch {
            return 0;
        };
        return count;
    }

    pub fn findX_Mas(self: Data) u16 {
        return self.findCrossMas();
    }
    pub fn addLine(self: *Data, line: []const u8) !void {
        var list = std.ArrayList(u8).init(self.alloc);
        errdefer list.deinit();

        for (line) |c| {
            try list.append(c);
        }
        try self.grid.append(list);
    }

    pub fn init(alloc: std.mem.Allocator) Data {
        const grid = std.ArrayList(std.ArrayList(u8)).init(alloc);
        return .{
            .grid = grid,
            .alloc = alloc,
        };
    }

    pub fn deinit(self: Data) void {
        for (self.grid.items) |line| {
            line.deinit();
        }
        self.grid.deinit();
    }
};

pub fn main() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const alloc = gpa.allocator();
    const data = try readData(alloc);
    defer data.deinit();
    const p1 = data.findXmas();
    print("part 1 count: {d}\n", .{p1});
    const p2 = data.findX_Mas();
    print("part 2 count: {d}\n", .{p2});
}

fn readData(alloc: std.mem.Allocator) !Data {
    var file = try std.fs.cwd().openFile("data.txt", .{});
    defer file.close();

    var buf_read = std.io.bufferedReader(file.reader());
    var in_stream = buf_read.reader();
    var buf: [4096]u8 = undefined;

    var data = Data.init(alloc);
    errdefer data.deinit();

    while (try in_stream.readUntilDelimiterOrEof(&buf, '\n')) |line| {
        const trimmed = if (@import("builtin").os.tag == .windows)
            std.mem.trimRight(u8, line, "\r")
        else
            line;
        try data.addLine(trimmed);
    }

    return data;
}

fn getFrontBackData(alloc: std.mem.Allocator) !Data {
    var data = Data.init(alloc);
    errdefer data.deinit();
    try data.addLine("WORD               "); //1
    try data.addLine("   WORD   WORD     "); //2
    try data.addLine("                   "); //0
    try data.addLine("               WORD"); //1
    return data;
}

test "find normal" {
    const data = try getFrontBackData(std.testing.allocator);
    defer data.deinit();
    const val = try data.findWord("WORD");
    try std.testing.expectEqual(4, val);
}

test "find backward" {
    const data = try getFrontBackData(std.testing.allocator);
    defer data.deinit();
    const val = try data.findWord("DROW");
    try std.testing.expectEqual(4, val);
}

fn getUpDownData(alloc: std.mem.Allocator) !Data {
    var data = Data.init(alloc);
    errdefer data.deinit();

    //                      1201
    try data.addLine("W   ");
    try data.addLine("O   ");
    try data.addLine("RW  ");
    try data.addLine("DO  ");
    try data.addLine(" R  ");
    try data.addLine(" D  ");
    try data.addLine(" W  ");
    try data.addLine(" O W");
    try data.addLine(" R O");
    try data.addLine(" D R");
    try data.addLine("   W");
    try data.addLine("   O");
    try data.addLine("   R");
    try data.addLine("   D");
    return data;
}
test "find down" {
    const data = try getUpDownData(std.testing.allocator);
    defer data.deinit();
    const val = try data.findWord("WORD");
    try std.testing.expectEqual(4, val);
}

test "find up" {
    const data = try getUpDownData(std.testing.allocator);
    defer data.deinit();

    const val = try data.findWord("DROW");
    try std.testing.expectEqual(4, val);
}

// backward is \
fn getBackwardDiagData(alloc: std.mem.Allocator) !Data {
    var data = Data.init(alloc);
    errdefer data.deinit();
    // 10x10
    try data.addLine("W     W   ");
    try data.addLine(" O  W  O  ");
    try data.addLine("  R  O  R ");
    try data.addLine("   D  R  D");
    try data.addLine("   W   D  ");
    try data.addLine("    O     ");
    try data.addLine("W    RW   ");
    try data.addLine(" O    DO  ");
    try data.addLine("  R     R ");
    try data.addLine("   D     D");
    return data;
}
test "find \\ down" {
    const data = try getBackwardDiagData(std.testing.allocator);
    defer data.deinit();
    const val = try data.findWord("WORD");
    try std.testing.expectEqual(6, val);
}

test "find \\ up" {
    const data = try getBackwardDiagData(std.testing.allocator);
    defer data.deinit();

    const val = try data.findWord("DROW");
    try std.testing.expectEqual(6, val);
}
// forward is /
fn getForwardDiagData(alloc: std.mem.Allocator) !Data {
    var data = Data.init(alloc);
    errdefer data.deinit();
    // 10x10
    try data.addLine("   W     W");
    try data.addLine("  O     O ");
    try data.addLine(" R    WR  ");
    try data.addLine("D    OD   ");
    try data.addLine("    R W   ");
    try data.addLine("   D O    ");
    try data.addLine("   WR    W");
    try data.addLine("  OD    O ");
    try data.addLine(" R     R  ");
    try data.addLine("D     D   ");
    return data;
}
test "find / down" {
    const data = try getForwardDiagData(std.testing.allocator);
    defer data.deinit();
    const val = try data.findWord("WORD");
    try std.testing.expectEqual(6, val);
}

test "find / up" {
    const data = try getForwardDiagData(std.testing.allocator);
    defer data.deinit();

    const val = try data.findWord("DROW");
    try std.testing.expectEqual(6, val);
}

fn getExampleOneData(alloc: std.mem.Allocator) !Data {
    var data = Data.init(alloc);
    errdefer data.deinit();
    try data.addLine("MMMSXXMASM");
    try data.addLine("MSAMXMSMSA");
    try data.addLine("AMXSXMAAMM");
    try data.addLine("MSAMASMSMX");
    try data.addLine("XMASAMXAMM");
    try data.addLine("XXAMMXXAMA");
    try data.addLine("SMSMSASXSS");
    try data.addLine("SAXAMASAAA");
    try data.addLine("MAMMMXMMMM");
    try data.addLine("MXMXAXMASX");
    return data;
}

test "example part 1" {
    const data = try getExampleOneData(std.testing.allocator);
    defer data.deinit();
    const val = data.findXmas();
    try std.testing.expectEqual(18, val);
}

// ex 1 data with last line
fn getExampleTwoData(alloc: std.mem.Allocator) !Data {
    var data = Data.init(alloc);
    errdefer data.deinit();
    try data.addLine("MMMSXXMASM");
    try data.addLine("MSAMXMSMSA");
    try data.addLine("AMXSXMAAMM");
    try data.addLine("MSAMASMSMX");
    try data.addLine("XMASAMXAMM");
    try data.addLine("XXAMMXXAMA");
    try data.addLine("SMSMSASXSS");
    try data.addLine("SAXAMASAAA");
    try data.addLine("MAMMMXMMMM");
    return data;
}

test "example part 2" {
    const data = try getExampleOneData(std.testing.allocator);
    defer data.deinit();
    const val = data.findX_Mas();
    try std.testing.expectEqual(9, val);
}
