const std = @import("std");
const Allocator = std.mem.Allocator;

const Data = @This();
alloc: Allocator,
comes_before: std.ArrayList([]u1),
comes_after: std.ArrayList([]u1),
has_any_before_rules: []u1,
has_any_after_rules: []u1,
print_job: std.ArrayList(std.ArrayList(u8)),

fn checkValue(v: u8) !void {
    if (v < 10 or v >= 100) {
        return error.ValueOutOfRange;
    }
}

fn itemMustBeBeforeSecondItem(self: Data, lhs: u8, rhs: u8) !bool {
    try checkValue(lhs);
    try checkValue(rhs);
    return self.comes_before.items[lhs - 10][rhs - 10] == 1;
}

fn hasIsBeforeRule(self: Data, v: u8) !bool {
    try checkValue(v);
    return self.has_any_before_rules[v - 10] == 1;
}

fn itemMustBeAfterSecondItem(self: Data, item: u8, after_item: u8) !bool {
    try checkValue(item);
    try checkValue(after_item);
    return self.comes_after.items[item - 10][after_item - 10] == 1;
}

fn hasIsAfterRule(self: Data, v: u8) !bool {
    try checkValue(v);
    return self.has_any_after_rules[v - 10] == 1;
}

pub fn addRule(self: *Data, rule: []const u8) !void {
    var before: u8 = try std.fmt.parseInt(u8, rule[0..2], 10);
    var after: u8 = try std.fmt.parseInt(u8, rule[3..], 10);
    before -= 10;
    after -= 10;

    self.has_any_before_rules[before] = 1;
    self.has_any_after_rules[after] = 1;

    self.comes_before.items[before][after] = 1;
    self.comes_after.items[after][before] = 1;
}

pub fn addPrintJob(self: *Data, job: []const u8) !void {
    var it = std.mem.splitSequence(u8, job, ",");
    var list = std.ArrayList(u8).init(self.alloc);
    errdefer list.deinit();

    while (it.next()) |page| {
        const p = try std.fmt.parseInt(u8, page, 10);
        try list.append(p);
    }
    try self.print_job.append(list);
}

fn beforeRulesValid(self: Data, page: u8, pages_after: []u8) !bool {
    for (pages_after) |pa| {
        if (try self.itemMustBeAfterSecondItem(page, pa)) {
            return false;
        }
    }
    //   75, 47, 61, 53, 29
    return true;
}
fn afterRulesValid(self: Data, page: u8, pages_before: []u8) !bool {
    for (pages_before) |pb| {
        if (try self.itemMustBeBeforeSecondItem(page, pb)) {
            return false;
        }
    }

    return true;
}
fn doesJobViolatePart1Rules(self: Data, job: std.ArrayList(u8)) bool {
    for (job.items, 0..) |page, i| {
        const pages_before = job.items[0..i];
        const pages_after = job.items[i + 1 ..];

        const after_ok = self.afterRulesValid(page, pages_before) catch false;
        if (!after_ok) {
            return true;
        }
        const before_ok = self.beforeRulesValid(page, pages_after) catch false;
        if (!before_ok) {
            return true;
        }
    }
    return false;
}

fn fixJob(self: Data, job: std.ArrayList(u8)) !std.ArrayList(u8) {
    // var fixed = try job.clone();

    var restart = false;
    var i: usize = 0;
    while (i < job.items.len) {
        var j: usize = i + 1;
        while (j < job.items.len) {
            defer j += 1;
            if (i == j) {
                continue;
            }
            const current_page = job.items[i];
            const other_page = job.items[j];
            if (i < j and try self.itemMustBeAfterSecondItem(other_page, current_page)) {
                job.items[i] = job.items[j];
                job.items[j] = current_page;
                restart = true;
                break;
            }
            if (i > j and try self.itemMustBeBeforeSecondItem(other_page, current_page)) {
                job.items[i] = job.items[j];
                job.items[j] = current_page;
                restart = true;
                break;
            }
        }
        if (restart) {
            restart = false;
            i = 0;
            continue;
        } else {
            i += 1;
        }
    }
    return job;
}
pub fn calcPart2Value(self: Data) !u32 {
    var total: u32 = 0;
    for (self.print_job.items) |job| {
        if (self.doesJobViolatePart1Rules(job)) {
            const fixed = try self.fixJob(job);
            const middle = fixed.items[@divTrunc(fixed.items.len, 2)];
            total += middle;
        }
    }

    return total;
}
pub fn calcPart1Value(self: Data) u32 {
    var total: u32 = 0;
    for (self.print_job.items) |job| {
        const middle = job.items[@divTrunc(job.items.len, 2)];

        if (!self.doesJobViolatePart1Rules(job)) {
            total += middle;
        }
    }
    return total;
}

pub fn init(alloc: Allocator) !Data {
    var print_job = std.ArrayList(std.ArrayList(u8)).init(alloc);
    errdefer print_job.deinit();

    var comes_before = std.ArrayList([]u1).init(alloc);
    errdefer comes_before.deinit();

    const has_before = try alloc.alloc(u1, 90);
    errdefer alloc.free(has_before);
    @memset(has_before, 0);

    const has_after = try alloc.alloc(u1, 90);
    errdefer alloc.free(has_after);
    @memset(has_after, 0);

    var comes_after = std.ArrayList([]u1).init(alloc);
    errdefer comes_after.deinit();

    for (10..100) |_| {
        const a: []u1 = try alloc.alloc(u1, 90);
        errdefer alloc.free(a);
        @memset(a, 0);
        try comes_after.append(a);

        const b: []u1 = try alloc.alloc(u1, 90);
        errdefer alloc.free(b);
        @memset(b, 0);
        try comes_before.append(b);
    }

    return .{
        .alloc = alloc,
        .comes_after = comes_after,
        .comes_before = comes_before,
        .has_any_after_rules = has_after,
        .has_any_before_rules = has_before,
        .print_job = print_job,
    };
}

pub fn deinit(self: Data) void {
    for (self.print_job.items) |job| {
        job.deinit();
    }
    self.print_job.deinit();

    for (10..100) |i| {
        self.alloc.free(self.comes_before.items[i - 10]);
        self.alloc.free(self.comes_after.items[i - 10]);
    }
    self.comes_before.deinit();
    self.comes_after.deinit();
    self.alloc.free(self.has_any_before_rules);
    self.alloc.free(self.has_any_after_rules);
}

test "is before" {
    var data = try Data.init(std.testing.allocator);
    defer data.deinit();

    try data.addRule("10|20");
    try data.addRule("11|20");
    try data.addRule("11|21");
    try data.addRule("11|23");

    try std.testing.expectEqual(true, try data.itemMustBeBeforeSecondItem(10, 20));
    try std.testing.expectEqual(true, try data.itemMustBeBeforeSecondItem(11, 20));
    try std.testing.expectEqual(true, try data.itemMustBeBeforeSecondItem(11, 21));

    try std.testing.expectEqual(false, try data.itemMustBeBeforeSecondItem(19, 20));
    try std.testing.expectEqual(false, try data.itemMustBeBeforeSecondItem(11, 22));
    try std.testing.expectEqual(false, try data.itemMustBeBeforeSecondItem(10, 11));
    try std.testing.expectEqual(false, try data.itemMustBeBeforeSecondItem(90, 20));

    try std.testing.expectError(error.ValueOutOfRange, data.itemMustBeBeforeSecondItem(9, 20));
    try std.testing.expectError(error.ValueOutOfRange, data.itemMustBeBeforeSecondItem(91, 2));
}

test "has before" {
    var data = try Data.init(std.testing.allocator);
    defer data.deinit();

    try data.addRule("10|20");
    try data.addRule("10|11");
    try data.addRule("11|20");
    try data.addRule("11|21");
    try data.addRule("11|23");

    try std.testing.expectEqual(true, try data.hasIsBeforeRule(10));
    try std.testing.expectEqual(true, try data.hasIsBeforeRule(11));
    try std.testing.expectEqual(false, try data.hasIsBeforeRule(20));
    try std.testing.expectEqual(false, try data.hasIsBeforeRule(21));
    try std.testing.expectEqual(false, try data.hasIsBeforeRule(23));
    try std.testing.expectEqual(false, try data.hasIsBeforeRule(80));

    try std.testing.expectError(error.ValueOutOfRange, data.hasIsBeforeRule(1));
}

test "has after" {
    var data = try Data.init(std.testing.allocator);
    defer data.deinit();

    try data.addRule("10|20");
    try data.addRule("10|11");
    try data.addRule("11|20");
    try data.addRule("11|21");
    try data.addRule("11|23");

    try std.testing.expectEqual(false, try data.hasIsAfterRule(10));
    try std.testing.expectEqual(true, try data.hasIsAfterRule(11));
    try std.testing.expectEqual(true, try data.hasIsAfterRule(20));
    try std.testing.expectEqual(true, try data.hasIsAfterRule(21));
    try std.testing.expectEqual(true, try data.hasIsAfterRule(23));
    try std.testing.expectEqual(false, try data.hasIsAfterRule(80));

    try std.testing.expectError(error.ValueOutOfRange, data.hasIsBeforeRule(1));
}

test "is after" {
    var data = try Data.init(std.testing.allocator);
    defer data.deinit();

    try data.addRule("10|20");
    try data.addRule("11|20");
    try data.addRule("11|21");
    try data.addRule("11|23");

    try std.testing.expectEqual(false, try data.itemMustBeAfterSecondItem(10, 20));
    try std.testing.expectEqual(false, try data.itemMustBeAfterSecondItem(11, 20));
    try std.testing.expectEqual(false, try data.itemMustBeAfterSecondItem(11, 21));
    try std.testing.expectEqual(false, try data.itemMustBeAfterSecondItem(11, 22));
    try std.testing.expectEqual(false, try data.itemMustBeAfterSecondItem(19, 20));
    try std.testing.expectEqual(false, try data.itemMustBeAfterSecondItem(10, 11));

    try std.testing.expectEqual(true, try data.itemMustBeAfterSecondItem(20, 10));
    try std.testing.expectEqual(true, try data.itemMustBeAfterSecondItem(20, 11));
    try std.testing.expectEqual(true, try data.itemMustBeAfterSecondItem(23, 11));

    try std.testing.expectError(error.ValueOutOfRange, data.itemMustBeBeforeSecondItem(100, 20));
    try std.testing.expectError(error.ValueOutOfRange, data.itemMustBeBeforeSecondItem(91, 2));
}
