import hashlib

SHARDS = ["shard-0", "shard-1", "shard-2", "shard-3"]


class ShardRouter:
    """Маршрутизатор SFMShop: определяет шард для пользователя и заказов."""

    def __init__(self, shards):
        self.shards = shards

    def shard_for_user(self, user_id):
        """Hash sharding по user_id (стабильный хеш md5)."""
        digest = hashlib.md5(str(user_id).encode()).hexdigest()
        index = int(digest, 16) % len(self.shards)
        return self.shards[index]

    def shard_for_order(self, user_id):
        """Заказы пользователя живут на том же шарде, что и сам пользователь."""
        return self.shard_for_user(user_id)

    def distribution(self, user_ids):
        """Сколько пользователей попало на каждый шард."""
        counts = {shard: 0 for shard in self.shards}
        for uid in user_ids:
            counts[self.shard_for_user(uid)] += 1
        return counts


router = ShardRouter(SHARDS)

users = [101, 102, 103, 104, 105, 106, 107, 108]

for uid in users:
    print(f"user {uid} -> {router.shard_for_user(uid)}")

# JOIN orders + users остаётся в пределах одного шарда
print("orders user 101 ->", router.shard_for_order(101))
print("same shard as user 101:", router.shard_for_order(101) == router.shard_for_user(101))

print("distribution:", router.distribution(users))
