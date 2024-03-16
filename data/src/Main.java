/*public class Main {
    public static void main(String[] args) {
        DoubleLinkedL<String> list = new LinkedList<>();
        list.insertAtFront("Node 1");
        list.insertAtFront("Node 2");
        list.insertAtFront("Node 3");

        System.out.println("First element: " + list.get(0));
        System.out.println("List size: " + list.getSize());

        list.deleteFromFront();
        System.out.println("First element after deletion: " + list.get(0));
        System.out.println("List size after deletion: " + list.getSize());
    }
}*/
public class HashTableTest {
    public static void main(String[] args) {
        // Test LinearProbingHashTable
        System.out.println("Testing LinearProbingHashTable:");
        LinearProbingHashTable<String, String> linearProbingHashTable = new LinearProbingHashTable<>(5);
        linearProbingHashTable.insert("key1", "value1");
        linearProbingHashTable.insert("key2", "value2");
        linearProbingHashTable.insert("key3", "value3"); // This should cause a collision
        linearProbingHashTable.insert("key4", "value4");
        linearProbingHashTable.insert("key5", "value5"); // This should trigger a resize

        System.out.println("Search result for 'key3': " + linearProbingHashTable.search("key3"));
        linearProbingHashTable.delete("key3");
        System.out.println("Search result for 'key3' after deletion: " + linearProbingHashTable.search("key3"));

        // Test ChainingHashTable
        System.out.println("\nTesting ChainingHashTable:");
        ChainingHashTable<String, String> chainingHashTable = new ChainingHashTable<>(5);
        chainingHashTable.insert("key1", "value1");
        chainingHashTable.insert("key2", "value2");
        chainingHashTable.insert("key3", "value3"); // This should cause a collision
        chainingHashTable.insert("key4", "value4");
        chainingHashTable.insert("key5", "value5"); // This should not trigger a resize

        System.out.println("Search result for 'key3': " + chainingHashTable.search("key3"));
        chainingHashTable.delete("key3");
        System.out.println("Search result for 'key3' after deletion: " + chainingHashTable.search("key3"));

        // Display the inner structure of the hash tables
        System.out.println("\nInner structure of LinearProbingHashTable:");
        linearProbingHashTable.displayStructure();

        System.out.println("\nInner structure of ChainingHashTable:");
        chainingHashTable.displayStructure();
    }
}

    // Add the following method inside the LinearProbingHashTable class:
    public void displayStructure() {
        System.out.println("Table structure:");
        for (int i = 0; i < capacity; i++) {
            if (keys[i] != null) {
                System.out.println("Index " + i + ": Key = " + keys[i] + ", Value = " + values[i]);
            } else {
                System.out.println("Index " + i + ": null");
            }
        }
    }

    // Add the following method inside the ChainingHashTable class:
    public void displayStructure() {
        System.out.println("Table structure:");
        for (int i = 0; i < capacity; i++) {
            System.out.print("Index " + i + ": ");
            for (Entry<K, V> entry : table[i]) {
                System.out.print("[Key = " + entry.key + ", Value = " + entry.value + "] -> ");
            }
            System.out.println("null");
        }
    }
