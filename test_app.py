#!/usr/bin/env python3
"""
Simple test script to verify the address book application works correctly.
"""

import sys
import json
from app import create_app

def test_address_book():
    """Test the address book functionality"""
    print("=" * 50)
    print("TESTING ADDRESS BOOK APPLICATION")
    print("=" * 50)
    
    try:
        # Create the Flask app
        app = create_app()
        print("✓ App created successfully!")
        
        # Create test client
        with app.test_client() as client:
            
            # Test 1: Health check
            print("\n1. Testing health check...")
            response = client.get('/health')
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                data = response.get_json()
                print(f"   Response: {json.dumps(data, indent=2)}")
                print("   ✓ Health check passed!")
            else:
                print("   ✗ Health check failed!")
                return False
            
            # Test 2: Create contacts
            print("\n2. Testing create contacts...")
            create_data = [
                {
                    "name": "Alice Smith",
                    "phone": "1234567890",
                    "email": "alice@example.com"
                },
                {
                    "name": "Bob Jones",
                    "phone": "2345678901", 
                    "email": "bob@example.com"
                }
            ]
            
            response = client.post('/create', json=create_data)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 201:
                contacts = response.get_json()
                print(f"   Created {len(contacts)} contacts")
                for contact in contacts:
                    print(f"   - {contact['name']} (ID: {contact['id'][:8]}...)")
                print("   ✓ Create contacts passed!")
                
                # Store IDs for later tests
                alice_id = contacts[0]['id']
                bob_id = contacts[1]['id']
            else:
                print(f"   ✗ Create contacts failed: {response.get_json()}")
                return False
            
            # Test 3: Search contacts
            print("\n3. Testing search contacts...")
            search_data = {"query": "Smith"}
            response = client.post('/search', json=search_data)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                results = response.get_json()
                print(f"   Found {len(results)} contacts for 'Smith'")
                for contact in results:
                    print(f"   - {contact['name']} ({contact['email']})")
                print("   ✓ Search contacts passed!")
            else:
                print(f"   ✗ Search contacts failed: {response.get_json()}")
                return False
            
            # Test 4: Update contacts
            print("\n4. Testing update contacts...")
            update_data = [
                {
                    "id": alice_id,
                    "phone": "9999999999"
                }
            ]
            
            response = client.put('/update', json=update_data)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                updated_contacts = response.get_json()
                print(f"   Updated {len(updated_contacts)} contacts")
                for contact in updated_contacts:
                    print(f"   - {contact['name']}: phone updated to {contact['phone']}")
                print("   ✓ Update contacts passed!")
            else:
                print(f"   ✗ Update contacts failed: {response.get_json()}")
                return False
            
            # Test 5: Delete contacts
            print("\n5. Testing delete contacts...")
            delete_data = [bob_id]
            
            response = client.delete('/delete', json=delete_data)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.get_json()
                print(f"   Deleted {result['deleted']} contacts")
                print("   ✓ Delete contacts passed!")
            else:
                print(f"   ✗ Delete contacts failed: {response.get_json()}")
                return False
            
            # Test 6: Verify deletion with search
            print("\n6. Verifying deletion with search...")
            search_data = {"query": "Bob"}
            response = client.post('/search', json=search_data)
            
            if response.status_code == 200:
                results = response.get_json()
                print(f"   Found {len(results)} contacts for 'Bob' (should be 0)")
                if len(results) == 0:
                    print("   ✓ Deletion verification passed!")
                else:
                    print("   ✗ Deletion verification failed!")
                    return False
            else:
                print(f"   ✗ Search after deletion failed: {response.get_json()}")
                return False
        
        print("\n" + "=" * 50)
        print("🎉 ALL TESTS PASSED! The address book is working correctly!")
        print("=" * 50)
        return True
        
    except Exception as e:
        print(f"\n✗ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    success = test_address_book()
    sys.exit(0 if success else 1) 