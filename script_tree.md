TOP :: PolicyReader
	class :: type :: Planning (if it can be recognized autmatically)
		function :: .parse (generate following )
		class :: element :: Document
			attr :: .content --str
			attr :: .doctype --str(planning or else)
			attr :: .title --str
			attr :: .vocab --dist
			attr :: .verb --list
			attr :: .rhetoric --list
			attr :: .time --Time
			attr :: .department --list
			attr :: .entity --dict:key=name,value=class(Entity)
			function :: .query(word) --show statistics and structure
			function :: .__getrhetoric__ (call .Rhetoric)
			function :: .__getverb__
			function :: .__getentity__
			function :: .__gettime__
			function :: .__getdepartment__

		class :: element :: Rhetoric
			attr :: .name
			attr :: .tag
			#attr :: .oc (object complement)
			#attr :: .nc (noun complement)

		class :: element :: Verb
			attr :: .name
			attr :: .tag # 对应的动词词性

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


