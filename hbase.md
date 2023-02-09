## Hbase

NoSQL database built on Hadoop, based on Google's BigTable.

- all it offers is API for CRUD
- no query language

### Data Model

- each row has unique key
- keys are sorted lexicographically, design key to minimize disk seek jump
- each row has a small number of col families
- each family contains LARGE number of columns
- each cell can have many versions with timestamps

### Google Use Case Example

Dataset storing web pages and versions

- key stored in reverse domain: `com.cnn.www`
- two families: contents, anchor
  - contents family has one column: content, store multiple version of web page
  - anchor family can have millions of web site domain as column name, anchor text as cell
