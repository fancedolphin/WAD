public class LinearProbingHashTable<K, V> {
    private static final int DEFAULT_CAPACITY = 20;
    private int capacity;
    private int size;
    private K[] keys;
    private V[] values;

    public LinearProbingHashTable() {
        this(DEFAULT_CAPACITY);
    }

    public LinearProbingHashTable(int capacity) {
        this.capacity = capacity;
        keys = (K[]) new Object[capacity];
        values = (V[]) new Object[capacity];
    }

    private int hash(K key) {
        return (key.toString().length() * 31) % capacity;
    }

    public void insert(K key, V value) {
        if (key == null) throw new IllegalArgumentException("Key cannot be null");
        if (size >= capacity * 0.75) resize(capacity * 2);

        int i;
        for (i = hash(key); keys[i] != null; i = (i + 1) % capacity) {
            if (keys[i].equals(key)) {
                values[i] = value;
                return;
            }
        }

        keys[i] = key;
        values[i] = value;
        size++;
        displayLoadFactor();
    }

    public V search(K key) {
        for (int i = hash(key); keys[i] != null; i = (i + 1) % capacity) {
            if (keys[i].equals(key)) {
                return values[i];
            }
        }
        return null;
    }

    public void delete(K key) {
        if (!contains(key)) {
            throw new RuntimeException("Key not found: " + key);
        }

        int i = hash(key);
        while (!key.equals(keys[i])) {
            i = (i + 1) % capacity;
        }

        keys[i] = null;
        values[i] = null;

        i = (i + 1) % capacity;
        while (keys[i] != null) {
            K keyToRehash = keys[i];
            V valToRehash = values[i];
            keys[i] = null;
            values[i] = null;
            size--;
            insert(keyToRehash, valToRehash);
            i = (i + 1) % capacity;
        }

        size--;
        if (size > 0 && size <= capacity / 8) resize(capacity / 2);
        displayLoadFactor();
    }

    private boolean contains(K key) {
        return search(key) != null;
    }

    private void resize(int newCapacity) {
        LinearProbingHashTable<K, V> temp = new LinearProbingHashTable<>(newCapacity);
        for (int i = 0; i < capacity; i++) {
            if (keys[i] != null) {
                temp.insert(keys[i], values[i]);
            }
        }
        keys = temp.keys;
        values = temp.values;
        capacity = temp.capacity;
    }

    private void displayLoadFactor() {
        System.out.println("Load factor: " + (double) size / capacity);
    }
}