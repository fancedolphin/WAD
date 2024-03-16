public class ChainingHashTable<K, V> {
    private static final int DEFAULT_CAPACITY = 8;
    private LinkedList<Entry<K, V>>[] table;
    private int size;
    private int capacity;

    public ChainingHashTable() {
        this(DEFAULT_CAPACITY);
    }

    public ChainingHashTable(int capacity) {
        this.capacity = capacity;
        table = (LinkedList<Entry<K, V>>[]) new LinkedList[capacity];
        for (int i = 0; i < capacity; i++) {
            table[i] = new LinkedList<>();
        }
    }

    private int hash(K key) {
        int hashValue = 0;
        String keyString = key.toString();
        for (int i = 0; i < keyString.length(); i++) {
            hashValue = (hashValue + keyString.charAt(i) * i) % capacity;
        }
        return hashValue;
    }

    public void insert(K key, V value) {
        if (key == null) throw new IllegalArgumentException("Key cannot be null");
        int index = hash(key);
        for (Entry<K, V> entry : table[index]) {
            if (entry.key.equals(key)) {
                entry.value = value;
                return;
            }
        }
        table[index].insertAtFront(new Entry<>(key, value));
        size++;
        if ((1.0 * size) / capacity >= 0.75) {
            resize(2 * capacity);
        }
        displayLoadFactor();
    }

    public V search(K key) {
        int index = hash(key);
        for (Entry<K, V> entry : table[index]) {
            if (entry.key.equals(key)) {
                return entry.value;
            }
        }
        return null;
    }

    public void delete(K key) {
        int index = hash(key);
        LinkedList<Entry<K, V>> entries = table[index];
        for (int i = 0; i < entries.getSize(); i++) {
            if (entries.get(i).key.equals(key)) {
                entries.delete(i);
                size--;
                displayLoadFactor();
                return;
            }
        }
        throw new RuntimeException("Key not found: " + key);
    }

    private void resize(int newCapacity) {
        ChainingHashTable<K, V> temp = new ChainingHashTable<>(newCapacity);
        for (LinkedList<Entry<K, V>> bucket : table) {
            for (Entry<K, V> entry : bucket) {
                temp.insert(entry.key, entry.value);
            }
        }
        table = temp.table;
        capacity = temp.capacity;
    }

    private void displayLoadFactor() {
        System.out.println("Load factor: " + (double) size / capacity);
    }

    private static class Entry<K, V> {
        K key;
        V value;

        Entry(K key, V value) {
            this.key = key;
            this.value = value;
        }
    }
}

