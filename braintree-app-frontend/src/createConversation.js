import React, { useState } from "react";

function CreateConversation({ currentUserId }) {
  const [query, setQuery] = useState("");
  const [searchResults, setSearchResults] = useState([]);
  const [selectedUsers, setSelectedUsers] = useState([]);

  // Search handler
  const handleSearch = async () => {
    const res = await fetch(`/api/users?query=${query}`);
    const data = await res.json();
    setSearchResults(data);
  };

  // Toggle user selection
  const toggleUser = (user) => {
    const exists = selectedUsers.find((u) => u.id === user.id);
    if (exists) {
      setSelectedUsers(selectedUsers.filter((u) => u.id !== user.id));
    } else {
      setSelectedUsers([...selectedUsers, user]);
    }
  };

  // Create conversation
  const createConversation = async () => {
    const userIds = selectedUsers.map((u) => u.id);
    const res = await fetch("/api/conversations", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ userIds }),
    });
    const convo = await res.json();
    console.log("Created conversation:", convo);
    // Redirect or update chat UI
  };

  return (
    <div className="p-4 max-w-md mx-auto">
      <h2 className="text-xl font-bold mb-2">Start a Group Chat</h2>
      <div className="flex gap-2">
        <input
          className="border p-2 flex-1"
          placeholder="Search users..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <button
          onClick={handleSearch}
          className="bg-blue-500 text-white px-3 py-1 rounded"
        >
          Search
        </button>
      </div>

      <div className="mt-3">
        <h3 className="font-semibold">Results:</h3>
        {searchResults.map((user) => (
          <div key={user.id} className="flex items-center gap-2 py-1">
            <input
              type="checkbox"
              checked={selectedUsers.some((u) => u.id === user.id)}
              onChange={() => toggleUser(user)}
            />
            <span>
              {user.name} ({user.email})
            </span>
          </div>
        ))}
      </div>

      {selectedUsers.length > 0 && (
        <>
          <div className="mt-3">
            <h3 className="font-semibold">Selected Users:</h3>
            <div className="flex flex-wrap gap-2 mt-1">
              {selectedUsers.map((user) => (
                <span
                  key={user.id}
                  className="bg-gray-200 px-2 py-1 rounded text-sm"
                >
                  {user.name}
                </span>
              ))}
            </div>
          </div>

          <button
            onClick={createConversation}
            className="mt-4 bg-green-500 text-white px-4 py-2 rounded"
          >
            Create Conversation
          </button>
        </>
      )}
    </div>
  );
}

export default CreateConversation;
