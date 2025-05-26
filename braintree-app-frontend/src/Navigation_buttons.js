import { Link } from "react-router-dom";

const Navigation = ({ isLoggedIn }) => (
  <nav
    style={{
      background: "#f8f9fa",
      padding: "1rem",
      marginBottom: "2rem",
      boxShadow: "0 2px 4px rgba(0,0,0,0.1)",
    }}
  >
    <div
      style={{
        display: "flex",
        justifyContent: "center",
        gap: "1rem",
      }}
    >
      {isLoggedIn ? (
        <>
          <Link to="/">
            <button
              style={{
                padding: "0.5rem 1rem",
                fontSize: "1rem",
                backgroundColor: "#007bff",
                color: "white",
                border: "none",
                borderRadius: "4px",
                cursor: "pointer",
                transition: "background-color 0.2s",
              }}
            >
              Payment
            </button>
          </Link>
          <Link to="/chat">
            <button
              style={{
                padding: "0.5rem 1rem",
                fontSize: "1rem",
                backgroundColor: "#28a745",
                color: "white",
                border: "none",
                borderRadius: "4px",
                cursor: "pointer",
                transition: "background-color 0.2s",
              }}
            >
              Chat
            </button>
          </Link>

          <Link to="/login">
            <button
              style={{
                padding: "0.5rem 1rem",
                fontSize: "1rem",
                backgroundColor: "#28a745",
                color: "red",
                border: "none",
                borderRadius: "4px",
                cursor: "pointer",
                transition: "background-color 0.2s",
              }}
            >
              Login
            </button>
          </Link>
        </>
      ) : null}

      {/* We need 2 buttons for login and register */}
      <Link to="/register">
        <button
          style={{
            padding: "0.5rem 1rem",
            fontSize: "1rem",
            backgroundColor: "#dc3545",
            color: "white",
            border: "none",
            borderRadius: "4px",
            cursor: "pointer",
            transition: "background-color 0.2s",
          }}
        >
          Register
        </button>
      </Link>
      <Link to="/login">
        <button
          style={{
            padding: "0.5rem 1rem",
            fontSize: "1rem",
            backgroundColor: "#dc3545",
            color: "white",
            border: "none",
            borderRadius: "4px",
            cursor: "pointer",
            transition: "background-color 0.2s",
          }}
        >
          {isLoggedIn ? "" : "Login"}
        </button>
      </Link>
    </div>
  </nav>
);

export default Navigation;
