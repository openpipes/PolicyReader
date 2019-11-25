TOP :: PolicyReader
    :extractor:
        - class :: type ::  EntityExtractor
            function :: dependencyExtract --return self.doc
            function :: embedding
            function :: keywordExtract --return self.doc
            function :: rhetoricExtractor --list
            function :: verbalExtractor --list
            function :: timeExtractor --list
            function :: nounExtractor --list
        

	planning - class :: type :: Planning (if it can be recognized autmatically)
		function :: .parse (generate following )
		class :: element :: Document
    		attr :: .archive --dict (vocabulary indexing)
    		attr :: .keywords --list (obtained from EntityExtractor,temporarily)
			attr :: .content --str
			attr :: .doctype --str(planning or else)
			attr :: .title --str
			attr :: .vocab --dist
			attr :: .noun --list
			attr :: .verb --list
			attr :: .rhetoric --list
			attr :: .terms --dict
			attr :: .time --Time
			attr :: .department --list
			attr :: .entity --dict:key=name,value=class(Entity)
			function :: .query(word) --show statistics and structure
			function :: .__getrhetoric__ (call .Rhetoric)
			function :: .__getverb__
			function :: .__getentity__
			function :: .__gettime__
			function :: .__getdepartment__
			
    type - class :: type :: Type
		class :: element :: Rhetoric
			attr :: .src
			attr :: .tar
			attr :: .srcType --POSTAG
			

		class :: element :: Verb
			attr :: .name
			attr :: .tag # 对应的动词词性

        class :: element :: Noun
            attr :: .name

		class :: element :: Entity
    		function :: .update (update index from database)
			attr :: .index (index from database)
			attr :: .name
			attr :: .tag 
			attr :: .triples --dict{"is_title_of":["XXX","yyy"]}/{"is_objective_of":["XXX"]}

		class :: element :: Time
			attr :: .year
			attr :: .month
			attr :: .day
			attr :: .hour
			attr :: .mintue
			attr :: .second

		class :: element :: Department
			attr :: .tier (national, provincial, city, county)
			attr :: .name

        class :: element :: University
            attr :: .name
            attr :: .location
            
        class :: element :: Location
            attr :: .name
            attr :: .province
            
        class :: element :: Enterprise
            attr :: .name
            attr :: .location


TOP :: 
	class :: tool :: Database
		class :: element :: sqlite
		class :: element :: mongodb

	class :: tool :: NLP
		class :: element :: 
		class :: element :: _predefined

	class :: tool :: Plot
	class :: tool :: Parser
	class :: tool :: utils
	class :: tool :: mthreadings


