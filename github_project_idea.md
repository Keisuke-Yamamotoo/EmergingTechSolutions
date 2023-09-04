
# Smart Contract for Tokenized Real Estate Investment

```
pragma solidity ^0.8.0;

contract TokenizedRealEstate {
    
    // Define the structure for a property
    struct Property {
        string propertyId;
        string location;
        uint256 price;
        address owner;
        bool isForSale;
    }

    // Define the structure for a token holder
    struct Holder {
        address holderAddress;
        uint256 balance;
    }

    // Mapping to store the list of properties
    mapping(string => Property) properties;

    // Mapping to store the list of holders and their token balances
    mapping(address => Holder) holders;

    // Event emitted when a property is listed for sale
    event PropertyListed(string propertyId, string location, uint256 price, address owner);

    // Event emitted when a property is sold
    event PropertySold(string propertyId, string location, uint256 price, address buyer);

    // Modifier to ensure that only the property owner can perform certain actions
    modifier onlyOwner(string memory propertyId) {
        require(properties[propertyId].owner == msg.sender, "Only the property owner can perform this action");
        _;
    }

    // Modifier to ensure that a property is listed for sale
    modifier propertyForSale(string memory propertyId) {
        require(properties[propertyId].isForSale, "Property is not listed for sale");
        _;
    }

    // Function to list a property for sale
    function listProperty(string memory propertyId, string memory location, uint256 price) public {
        require(properties[propertyId].owner == address(0), "Property with specified ID already exists");
        properties[propertyId] = Property(propertyId, location, price, msg.sender, true);
        emit PropertyListed(propertyId, location, price, msg.sender);
    }

    // Function to buy a property
    function buyProperty(string memory propertyId) public payable propertyForSale(propertyId) {
        Property storage property = properties[propertyId];
        require(msg.value >= property.price, "Insufficient funds to buy the property");
        require(msg.sender != property.owner, "Cannot buy your own property");
        
        // Transfer ownership of the property
        address previousOwner = property.owner;
        property.owner = msg.sender;
        property.isForSale = false;

        // Update balances of the buyer and previous owner
        holders[msg.sender].balance += msg.value;
        holders[previousOwner].balance -= property.price;

        // Emit the PropertySold event
        emit PropertySold(propertyId, property.location, property.price, msg.sender);
    }

    // Function to check the balance of a token holder
    function getBalance() public view returns (uint256) {
        return holders[msg.sender].balance;
    }

    // Function to withdraw funds from the token balance
    function withdrawFunds(uint256 amount) public {
        uint256 balance = holders[msg.sender].balance;
        require(amount <= balance, "Insufficient funds");
        
        // Update the balance and transfer the funds
        holders[msg.sender].balance -= amount;
        payable(msg.sender).transfer(amount);
    }
}
```

This project idea is to create a smart contract for tokenized real estate investment. The contract allows users to list their properties for sale and buy properties using cryptocurrency. The contract maintains a list of properties, including their location, price, and owner. It also tracks the token balance of each user, allowing them to withdraw their funds.

The contract provides the following functionalities:
- Listing a property for sale: Property owners can list their properties by providing the property ID, location, and price.
- Buying a property: Users can buy properties listed for sale by paying the specified price in cryptocurrency. Ownership of the property is transferred to the buyer, and the corresponding token balances are updated.
- Checking token balance: Users can check their token balance.
- Withdrawing funds: Users can withdraw funds from their token balance to their own address.

The contract uses Solidity and is ready to be deployed on Ethereum or any other compatible blockchain platform.
