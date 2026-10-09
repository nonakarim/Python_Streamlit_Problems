import streamlit as st
import time

# Page Configuration
st.set_page_config(
    page_title= "Smart Warehouse Inventory Manager",
    page_icon= "🏢",
    layout= "wide",
    initial_sidebar_state= "collapsed"
)

# Declaring data I want to survive rerun 

if "products_num" not in st.session_state:
    st.session_state.products_num = 0

if "total_quantity" not in st.session_state:
    st.session_state.total_quantity = 0

if "inventory_data" not in st.session_state:
    st.session_state.inventory_data = []

def side_bar():
    """shows Program Summary in sidebar"""

    # Displays Warehouse Name
    st.subheader("Warehouse Name")
    st.info("NoNa Warehouse")

    # Displays Total Number Of Products in NoNa Warehouse
    st.subheader("Total number of products")
    st.info(st.session_state.products_num)

    # Displays Total Quantity In NoNa Warehouse
    st.subheader("Total quantity in stock")
    st.info(st.session_state.total_quantity)

    # Page Selection
    choice = st.sidebar.selectbox("Main Sections", 
                     ["Add Product",
                      "View Inventory",
                      "Search Products",
                      "Stock Management",
                      "Update Product Price",
                      "Low-Stock Report",
                      "Inventory Statistics",
                      "Value by Category Report"])

    return choice

def data_enter_form():
    id = st.text_input("Product ID")
    name = st.text_input("Product Name")
    category = st.selectbox("Category", 
                            [
                                "Clothing",
                                "Electronics"
                            ])
    quantity = 0
    unit_price = st.number_input("Unit Price", min_value=1)
    add = st.form_submit_button("Add Product", type= "primary")

    return id, name, category, quantity, unit_price, add

def duplicateID(ID):
    for product in st.session_state.inventory_data:
        if product.get("ID") == ID:
            return True

    return False

def duplicateProduct(name):
    for product in st.session_state.inventory_data:
        if product.get("Name") == name:
            return True

    return False

def searchMethod():
    st.subheader("Use:")
    useID = st.checkbox("Product ID")
    useName = st.checkbox("Product Name")
    useCategory = st.checkbox("Product Category")

    return useID, useName, useCategory

def searchUsingID(searchID):
    search_list = []

    for id in st.session_state.inventory_data:
        if id.get("ID") == searchID:
            search_list.append(id)

    return search_list

def searchUsingName(searchName):
    search_list = []

    for name in st.session_state.inventory_data:
        if name.get("Name") == searchName:
            search_list.append(name)

    return search_list

def searchUsingCategory(searchCategory):
    search_list = []
    
    for category in st.session_state.inventory_data:
        if category.get("Category") == searchName:
            search_list.append(category)

    return search_list

def restock_product():
    st.header("A. Restock Product")
    
    names = []

    for name in st.session_state.inventory_data:
        names.append(name.get("Name"))

    product = st.selectbox("Products", names)
    new_quantity = st.number_input("Enter New Quantity", min_value= 1)
    restock = st.button("Restock", type= "primary")

    if restock:
        st.session_state.total_quantity += new_quantity

        for name in st.session_state.inventory_data:
            if name.get("Name") == product:
                name["Quantity"] += new_quantity

        st.rerun()

@st.dialog("Are You Sure You Want To Delete This Product", width= "small", dismissible= False)
def deletion():
    col1, col2 = st.columns(2)
    with col1:
        yes = st.button("Yes", type= "primary", width= 100)
    with col2:
        no = st.button("No", type= "primary", width= 100)

    if yes:
        for item in st.session_state.inventory_data:
            if item.get("Name") == products:
                st.session_state.total_quantity -= item.get("Quantity")
                st.session_state.products_num -= 1
                st.session_state.inventory_data.remove(item) 
                st.success("Product Deleted Successfully")
                break

        time.sleep(2)
        st.rerun()
    if no:
        st.rerun()

@st.dialog("Are You Sure You Want To Change This Product's Price", width= "small", dismissible= False)
def price_changing(price):
    col1, col2 = st.columns(2)
    with col1:
        yes = st.button("Yes", type= "primary", width= 100)
    with col2:
        no = st.button("No", type= "primary", width= 100)

    if yes:
        for item in st.session_state.inventory_data:
            if item.get("Name") == products:
                item["Unit Price"] = price
                st.success("This Product Price Was Changed Successfully")
        time.sleep(2)
        st.rerun()
    if no:
        st.rerun()

def value_by_category():
    clothing=0
    electronics=0

    for product in st.session_state.inventory_data:
        if product.get("category") == "Electronics":
            electronics += product.get("Unit Price")
        else:
            clothing += product.get("Unit Price")

    col1, col2, col3 = st.columns(3)
    with col2:
        with st.container(border=True):
            st.markdown(f"- **Electronics:** {electronics}")
            st.markdown(f"- **Clothing:** {clothing}")
    
st.title("🏢 Smart Warehouse Inventory Manager", text_alignment= "center")


with st.sidebar:
    choice = side_bar()

if choice == "Add Product":
    col1, col2, col3 = st.columns(3)

    with col2:
        st.header("➕ Add a New Product")
        with st.form("Add Product"):
            productID, productName, category, quantity, unit_price, add = data_enter_form()
    
            if(add):
                duplicatedID = duplicateID(productID)
                duplicatedProduct = duplicateProduct(productName)

                if not productID == "" and not productName == "":
                    if not duplicatedID and not duplicatedProduct:
                        
                        st.session_state.products_num += 1

                        st.session_state.inventory_data.append({
                            "ID": productID,
                            "Name": productName,
                            "Unit Price": unit_price,
                            "Quantity": quantity,
                            "category": category,
                        })
                        st.rerun()
                    else:
                        st.warning("Another product has the same ID or Name")
                else:
                    st.error("May NOT Leave Space Empty")
        
elif choice == "View Inventory":
    col1, col2, col3 = st.columns(3)
    st.header("📦 View Inventory")

    if st.session_state.inventory_data != []:
        st.table(st.session_state.inventory_data)
    else:
        st.info("No Products Yet")

elif choice == "Search Products":
    useID, useName, UseCategory = searchMethod()
    search_list = []
    
    IDs = []
    for id in st.session_state.inventory_data:
        IDs.append(id.get("ID"))

    names = []
    for name in st.session_state.inventory_data:
        names.append(name.get("Name"))

    categories = []
    for category in st.session_state.inventory_data:
        categories.append(category.get("category"))

    if useID:
        searchID = st.selectbox("Product ID", IDs)
        search_list.extend(searchUsingID(searchID))

    if useName:
        searchName = st.selectbox("Product Name", names)
        search_list.extend(searchUsingName(searchName))

    if UseCategory:
        searchCategory = st.selectbox("Product Category", categories)
        search_list.extend(searchUsingCategory(searchCategory))

    search = st.button("Search", type= "primary")
    if search:
        seen_ids = set()
        unique_products = []

        for product in search_list:
            product_id = product.get("ID")

        if product_id not in seen_ids:
            unique_products.append(product)
            seen_ids.add(product_id)
        
            st.table(unique_products)

if choice == "Stock Management":
    restock_product()
    st.header("B. Delete Product")
    
    names = []
    for name in st.session_state.inventory_data:
        names.append(name.get("Name"))

    products = st.selectbox("Select the product you want to delete", names)
    delete = st.button("Delete", type= "primary")
    
    if delete:
        for item in st.session_state.inventory_data:
            if item.get("Name") == products:
                st.table(item)
                break

        deletion()

if choice == "Update Product Price":
    names = []
    for name in st.session_state.inventory_data:
        names.append(name.get("Name"))

    products = st.selectbox("Select the product you want to change it's price", names)
    price = st.number_input("Enter the new price")
    change = st.button("Change", type= "primary")

    if change:
        price_changing(price)

if choice == "Low-Stock Report":
    threshold = st.number_input("Show products with stock below:")
    search = st.button("Search", key= "search", type= "primary", width= 100)
    report = []

    if search:
        for product in st.session_state.inventory_data:
            if product.get("Quantity") < threshold:
                report.append({
                                "Product": product.get("Name"),
                                "Quantity": product.get("Quantity")
                            })
        if report != []:
            st.table(report)
        else:
            st.success("All Products Currently Have Sufficient Stock")

if choice == "Inventory Statistics":
    col1, col2, col3 = st.columns(3)

    with col2:
        with st.container(border=True):
            st.subheader("1. Total Products")
            st.info(len(st.session_state.inventory_data))
            st.subheader("2. Total Quantity")
            st.info(st.session_state.total_quantity)

            st.subheader("3. Total Inventory Value")
            for product in st.session_state.inventory_data:
                st.write(product.get("Name"))
                st.info(product.get("Quantity") * product.get("Unit Price"))

            st.subheader("4. Highest Stock Product")
            maximum=0
            maximum_dict = {}
            for product in st.session_state.inventory_data:
                if product.get("Quantity") > maximum:
                    maximum = product.get("Quantity")
                    maximum_dict= product

            if maximum_dict != {}:
                st.table(maximum_dict)
            else:
                st.info("All Your Products Are Equaly Stocked")

            st.subheader("5. Lowest Stock Product")
            minimum=0
            minimum_dict = {}
            for product in st.session_state.inventory_data:
                minimum = product.get("Quantity")
                minimum_dict = product
                break

            for product in st.session_state.inventory_data:
                if product.get("Quantity") < minimum:
                    minimum = product.get("Quantity")
                    minimum_dict = product

            if minimum_dict != {}:
                st.table(minimum_dict)
            else:
                st.info("All Your Products Are Equaly Stocked")

if choice == "Value by Category Report":
    value_by_category()