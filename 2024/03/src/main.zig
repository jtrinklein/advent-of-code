const std = @import("std");

const OpType = enum { Mul, Do, Dont, Nop };
const Instruction = struct {
    lhs: i32,
    rhs: i32,
    optype: OpType,
    pub fn init(l: i32, r: i32) Instruction {
        return .{
            .lhs = l,
            .rhs = r,
            .optype = OpType.Mul,
        };
    }
};
const Token = enum(u8) {
    Any,
    M,
    U,
    L,
    OpenParen,
    CloseParen,
    LeftDigit,
    RightDigit,
    D,
    O,
    N,
    Quote,
    T,
    _,
};
const ParsingState = struct {
    next_token: Token = Token.Any,
    lhs: i32 = 0,
    rhs: i32 = 0,
    complete: bool = false,
    current_op: OpType = OpType.Nop,

    pub fn reset(self: *ParsingState) void {
        self.next_token = Token.Any;
        self.lhs = 0;
        self.rhs = 0;
        self.complete = false;
        self.current_op = OpType.Nop;
    }
};
const Data = struct {
    instructions: std.ArrayList(Instruction),
    parsing_state: ParsingState = .{},

    fn updateParseMulState(self: *Data, c: u8) void {
        switch (self.parsing_state.next_token) {
            .M => {
                if (c == 'm') {
                    self.parsing_state.next_token = Token.U;
                } else {
                    self.parsing_state.reset();
                    self.updateParseState(c);
                }
            },
            .U => {
                if (c == 'u') {
                    self.parsing_state.next_token = Token.L;
                } else {
                    self.parsing_state.reset();
                    self.updateParseState(c);
                }
            },
            .L => {
                if (c == 'l') {
                    self.parsing_state.next_token = Token.OpenParen;
                } else {
                    self.parsing_state.reset();
                    self.updateParseState(c);
                }
            },
            .OpenParen => {
                if (c == '(') {
                    self.parsing_state.next_token = Token.LeftDigit;
                    self.parsing_state.lhs = 0;
                } else {
                    self.parsing_state.reset();
                    self.updateParseState(c);
                }
            },
            .LeftDigit => {
                if (c == ',') {
                    self.parsing_state.next_token = Token.RightDigit;
                    self.parsing_state.rhs = 0;
                } else if (c >= '0' and c <= '9') {
                    const v: i32 = @intCast(c - '0');
                    self.parsing_state.lhs = self.parsing_state.lhs * 10 + v;
                } else {
                    self.parsing_state.reset();
                    self.updateParseState(c);
                }
            },
            .RightDigit => {
                if (c == ')') {
                    self.parsing_state.next_token = Token.M;
                    self.parsing_state.complete = true;
                } else if (c >= '0' and c <= '9') {
                    const v: i32 = @intCast(c - '0');
                    self.parsing_state.rhs = self.parsing_state.rhs * 10 + v;
                } else {
                    self.parsing_state.reset();
                    self.updateParseState(c);
                }
            },
            else => {
                self.parsing_state.reset();
                self.updateParseState(c);
            },
        }
    }

    fn updateParseDoDontState(self: *Data, c: u8) void {
        switch (self.parsing_state.next_token) {
            .D => {
                if (c == 'd') {
                    self.parsing_state.next_token = Token.O;
                } else {
                    self.parsing_state.reset();
                    self.updateParseState(c);
                }
            },
            .O => {
                if (c == 'o') {
                    self.parsing_state.next_token = Token.N;
                } else {
                    self.parsing_state.reset();
                    self.updateParseState(c);
                }
            },
            .N => {
                if (c == 'n') {
                    self.parsing_state.current_op = OpType.Dont;
                    self.parsing_state.next_token = Token.Quote;
                } else if (c == '(') {
                    self.parsing_state.current_op = OpType.Do;
                    self.parsing_state.next_token = Token.CloseParen;
                } else {
                    self.parsing_state.reset();
                    self.updateParseState(c);
                }
            },
            .Quote => {
                if (c == '\'') {
                    self.parsing_state.next_token = Token.T;
                } else {
                    self.parsing_state.reset();
                    self.updateParseState(c);
                }
            },
            .T => {
                if (c == 't') {
                    self.parsing_state.next_token = Token.OpenParen;
                } else {
                    self.parsing_state.reset();
                    self.updateParseState(c);
                }
            },
            .OpenParen => {
                if (c == '(') {
                    self.parsing_state.next_token = Token.CloseParen;
                } else {
                    self.parsing_state.reset();
                    self.updateParseState(c);
                }
            },
            .CloseParen => {
                if (c == ')') {
                    self.parsing_state.next_token = Token.Any;
                    self.parsing_state.complete = true;
                } else {
                    self.parsing_state.reset();
                    self.updateParseState(c);
                }
            },
            else => {
                self.parsing_state.reset();
                self.updateParseState(c);
            },
        }
    }

    fn updateParseState(self: *Data, c: u8) void {
        switch (self.parsing_state.current_op) {
            .Mul => {
                self.updateParseMulState(c);
            },
            .Do, .Dont => {
                self.updateParseDoDontState(c);
            },
            .Nop => {
                if (c == 'm') {
                    self.parsing_state.current_op = OpType.Mul;
                    self.parsing_state.next_token = Token.M;
                    self.updateParseMulState(c);
                } else if (c == 'd') {
                    self.parsing_state.current_op = OpType.Do;
                    self.parsing_state.next_token = Token.D;
                    self.updateParseDoDontState(c);
                }
            },
        }
    }
    pub fn parseProgramLine(self: *Data, line: []const u8) !void {
        for (line) |c| {
            self.updateParseState(c);
            if (self.parsing_state.complete) {
                try self.instructions.append(.{
                    .lhs = self.parsing_state.lhs,
                    .rhs = self.parsing_state.rhs,
                    .optype = self.parsing_state.current_op,
                });
                self.parsing_state.reset();
            }
        }
    }

    pub fn runProgram(self: Data, skip_do_dont: bool) i32 {
        var result: i32 = 0;

        var enabled = true;
        for (self.instructions.items) |ins| {
            switch (ins.optype) {
                .Mul => {
                    if (enabled) {
                        result += ins.lhs * ins.rhs;
                    }
                },
                .Do => {
                    enabled = true;
                },
                .Dont => {
                    enabled = skip_do_dont;
                },
                .Nop => {},
            }
        }
        return result;
    }

    pub fn init(alloc: std.mem.Allocator) Data {
        var parsing_state: ParsingState = .{};
        parsing_state.reset();
        return .{
            .parsing_state = parsing_state,
            .instructions = std.ArrayList(Instruction).init(alloc),
        };
    }
    pub fn deinit(self: Data) void {
        self.instructions.deinit();
    }
};

pub fn main() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();

    const alloc = gpa.allocator();
    const data = try readData(alloc);
    defer data.deinit();

    const p1 = data.runProgram(true);
    std.debug.print("part1: {d}\n", .{p1});
    const p2 = data.runProgram(false);
    std.debug.print("part2: {d}\n", .{p2});
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
        try data.parseProgramLine(trimmed);
    }

    return data;
}

test "example part 1" {
    var data = Data.init(std.testing.allocator);
    defer data.deinit();
    try data.parseProgramLine("xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))");
    const result = data.runProgram(true);
    try std.testing.expectEqual(161, result);
}

test "example part 2" {
    var data = Data.init(std.testing.allocator);
    defer data.deinit();
    try data.parseProgramLine("xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))");
    const result = data.runProgram(false);
    try std.testing.expectEqual(48, result);
}
